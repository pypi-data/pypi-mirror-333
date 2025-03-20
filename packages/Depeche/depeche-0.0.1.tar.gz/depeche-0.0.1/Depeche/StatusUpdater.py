import threading
import queue
import time
from StatusMessage import StatusMessage

class StatusUpdater:
	"""Handles concurrent message updates using a queue."""
	def __init__(self):
		self.message_queue = queue.Queue()
		self.running = threading.Event()
		self.running.set()
		self.lock = threading.Lock()

		self.consumer_thread = threading.Thread(target=self._consume_messages, daemon=True)
		self.consumer_thread.start()

	def add_message(self, message: str) -> StatusMessage:
		"""Creates and queues a new message."""
		msg = StatusMessage(message)
		self.message_queue.put(msg)
		return msg  # Return reference for potential stale marking

	def _consume_messages(self):
		"""Continuously processes messages from the queue."""
		while self.running.is_set():
			try:
				msg = self.message_queue.get(timeout=1)  # Wait for messages
				time.sleep(0.5)
				with self.lock:
					if msg.stale:
						print(f"Skipping stale message: {msg.id}")
						del msg
						continue
					else:
						print(f"Handling message: {msg.id} - {msg.message}")
						del msg  # Explicitly remove message after processing
			except queue.Empty:
				continue  # No messages, retry

	def stop(self):
		"""Stops the consumer thread."""
		self.running.clear()
		self.consumer_thread.join()

# Example usage
if __name__ == "__main__":
	updater = StatusUpdater()

	msg1 = updater.add_message("First update")
	msg2 = updater.add_message("Second update")
	msg3 = updater.add_message("Third update")
	time.sleep(0.1)  # Simulate delay

	msg2.mark_stale()  # Mark the second message as stale before it's handled
	time.sleep(1.5)  # Allow time for processing

	updater.stop()