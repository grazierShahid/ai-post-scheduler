from datetime import datetime, timezone
import threading
import time
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.post import Post
from app.models.enums import PostStatus


class PostPublisherScheduler:
    def __init__(self, interval_seconds: int = 10):
        self.interval_seconds = interval_seconds
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        while not self._stop_event.is_set():
            try:
                self._publish_due_posts()
            except Exception:
                pass
            time.sleep(self.interval_seconds)

    def _publish_due_posts(self):
        now = datetime.now(timezone.utc)
        db: Session = SessionLocal()
        try:
            q = (
                db.query(Post)
                .filter(Post.status == PostStatus.SCHEDULED)
                .filter(Post.schedule_time <= now)
            )
            posts = q.all()
            for p in posts:
                p.status = PostStatus.PUBLISHED
                p.published_at = now
                db.add(p)
            if posts:
                db.commit()
        finally:
            db.close() 