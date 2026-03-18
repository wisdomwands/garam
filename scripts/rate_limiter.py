import time
import collections

class TPMRateLimiter:
    def __init__(self, tpm_limit=30000, window_seconds=60):
        """
        Initializes the RateLimiter.
        :param tpm_limit: Token Per Minute limit.
        :param window_seconds: Time window in seconds (default 60s).
        """
        self.tpm_limit = tpm_limit
        self.window_seconds = window_seconds
        self.request_history = collections.deque() # Stores (timestamp, tokens)

    def wait_for_tokens(self, estimated_tokens):
        """
        Checks if the request can proceed. If not, sleeps until it can.
        """
        current_time = time.time()
        
        # Remove old requests outside the window
        while self.request_history and self.request_history[0][0] < current_time - self.window_seconds:
            self.request_history.popleft()

        # Calculate current usage
        current_usage = sum(tokens for _, tokens in self.request_history)
        
        if current_usage + estimated_tokens > self.tpm_limit:
            # Simple heuristic: wait until enough capacity frees up
            # In a real sliding window, we'd need to wait until the oldest request expires.
            # However, if the history is empty or we are just bursty, we might just sleep a bit.
            
            if self.request_history:
                oldest_time, _ = self.request_history[0]
                wait_time = (oldest_time + self.window_seconds) - current_time + 1 # +1 buffer
                if wait_time > 0:
                    print(f"[RateLimiter] TPM limit approaching ({current_usage}/{self.tpm_limit}). Sleeping for {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
            else:
                 # If history is empty but we still can't fit (single massive request?), just proceed or warn.
                 # But here it means we strictly enforce Limit. 
                 # If estimated > limit, we can never send it. Warning and simple sleep.
                 if estimated_tokens > self.tpm_limit:
                     print(f"[RateLimiter] Warning: Single request size ({estimated_tokens}) exceeds TPM limit ({self.tpm_limit}). Proceeding cautiously after 5s delay.")
                     time.sleep(5)

        # Record this request (optimistic: assuming it will be sent now)
        self.request_history.append((time.time(), estimated_tokens))

    def estimate_tokens(self, text):
        """
        Conservative estimate: 1 char ~= 0.5 tokens (English) or 1 char ~= 1 token (Korean/Unicode).
        Let's use a safe upper bound: 1 char = 1 token for Korean heavy text, or 0.7 mixed.
        """
        return int(len(text) * 0.7)
