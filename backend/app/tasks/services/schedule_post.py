from datetime import datetime, timezone
import asyncio
import json
from app.tasks.celery import celery_app
from app.database.session import SessionLocal
from app.crud.post import PostCRUD
from app.crud.social_platform import SocialPlatformCRUD
from app.core.mock_platforms import MockPlatformFactory, PlatformError
from app.models.enums import PostStatus
from app.utils.logger import get_logger

logger = get_logger(__name__)

@celery_app.task
def publish_post_task(post_id: int):
    """Fetches a scheduled post and publishes it to all its target social media platforms."""
    logger.info(f"Executing publish_post_task for post ID: {post_id}")
    db = SessionLocal()
    post_crud = PostCRUD(db)
    platform_crud = SocialPlatformCRUD(db)

    try:
        post = post_crud.get(post_id)

        if not post:
            logger.warning(f"Post {post_id} not found.")
            return f"Post {post_id} not found."

        if post.status != PostStatus.SCHEDULED:
            logger.warning(f"Post {post_id} is not in a scheduled state (current state: {post.status}). Aborting.")
            return f"Post {post_id} not in scheduled state."

        platforms = platform_crud.get_by_ids(post.platform_ids or [])
        if not platforms:
            raise ValueError("No valid platforms found for this post.")

        content_payload = {
            "text": post.content_text.get("text", ""),
        }
        if post.image:
            content_payload["image"] = post.image.path

        async def publish_to_platform(platform):
            logger.info(f"Publishing post {post_id} to {platform.type.value}...")
            mock_platform_api = MockPlatformFactory.get_platform(platform.type.value.lower())
            try:
                response = await mock_platform_api.post_content(content_payload)
                if response.success:
                    return {"platform": platform.type.value, "success": True, "details": response.data.get('post_id')}
                else:
                    return {"platform": platform.type.value, "success": False, "details": response.error}
            except PlatformError as e:
                return {"platform": platform.type.value, "success": False, "details": f"Platform Error: {e.message}"}
            except Exception as e:
                return {"platform": platform.type.value, "success": False, "details": f"Unexpected Error: {str(e)}"}

        # Run all platform publications concurrently
        async def main():
            return await asyncio.gather(*[publish_to_platform(p) for p in platforms])

        results = asyncio.run(main())

        successful_pubs = [res for res in results if res["success"]]
        failed_pubs = [res for res in results if not res["success"]]

        if not failed_pubs:
            post.status = PostStatus.PUBLISHED
            post.published_at = datetime.now(timezone.utc)
            post.remarks = json.dumps([res["details"] for res in successful_pubs])
            logger.info(f"Post {post_id} successfully published to all platforms.")
        else:
            post.status = PostStatus.FAILED
            post.remarks = json.dumps({
                "successes": [res["details"] for res in successful_pubs],
                "failures": [res["details"] for res in failed_pubs]
            })
            logger.error(f"Failed to publish post {post_id} to one or more platforms.")

        db.commit()
        return f"Processed post {post_id}. Successes: {len(successful_pubs)}, Failures: {len(failed_pubs)}."

    except Exception as e:
        post.status = PostStatus.FAILED
        post.remarks = f"A critical error occurred during publishing: {str(e)}"
        db.commit()
        logger.error(f"A critical error occurred while publishing post {post_id}: {e}", exc_info=True)
        return f"Critical error for post {post_id}."

    finally:
        db.close()


@celery_app.task
def check_scheduled_posts():
    """Periodic task to find and publish due posts."""
    logger.info("Checking for scheduled posts ready to be published...")
    db = SessionLocal()
    try:
        post_crud = PostCRUD(db)
        now_utc = datetime.now(timezone.utc)
        due_posts = post_crud.get_due_posts(now_utc)

        if not due_posts:
            logger.info("No posts are due for publishing.")
            return "No posts due."

        logger.info(f"Found {len(due_posts)} posts ready for publishing.")
        for post in due_posts:
            logger.info(f"Triggering publish task for post {post.id} (scheduled for {post.schedule_time})")
            publish_post_task.delay(post.id)
        
        return f"Triggered publishing for {len(due_posts)} posts."
    except Exception as e:
        logger.error(f"Error in check_scheduled_posts: {e}", exc_info=True)
        return f"Error: {str(e)}"
    finally:
        db.close()
