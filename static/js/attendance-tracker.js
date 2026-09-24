/**
 * DBERT Global Attendance Tracker
 * Automatically tracks active study & portal time across all pages on https://internship.dbert.online/
 * Pings /attendance/ping every 3 minutes when an intern is logged in.
 * Multi-tab safe via localStorage coordination.
 */
(function() {
    'use strict';

    const PING_INTERVAL_MS = 180000; // 3 minutes
    const LOCAL_STORAGE_KEY = 'dbert_last_attendance_ping';
    let _timer = null;

    async function sendAttendancePing() {
        // Prevent multi-tab spam: if another tab pinged less than 2.5 minutes ago, skip
        try {
            const lastPingStr = localStorage.getItem(LOCAL_STORAGE_KEY);
            if (lastPingStr) {
                const lastPing = parseInt(lastPingStr, 10);
                if (!isNaN(lastPing) && (Date.now() - lastPing) < 150000) {
                    return;
                }
            }
        } catch (e) {
            // localStorage might be unavailable or restricted, continue to ping
        }

        try {
            const res = await fetch('/attendance/ping', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' }
            });

            if (res.status === 401 || res.status === 403) {
                // Not logged in as an intern — stop timer on this page
                if (_timer) {
                    clearInterval(_timer);
                    _timer = null;
                }
                return;
            }

            if (!res.ok) return;

            const data = await res.json();
            if (data.status === 'success') {
                try {
                    localStorage.setItem(LOCAL_STORAGE_KEY, Date.now().toString());
                } catch (e) {}

                // If on the portal dashboard, update the live attendance counter
                if (typeof window.updateLiveCounter === 'function') {
                    window.updateLiveCounter(data.total_minutes);
                }
            } else if (data.reason === 'internship_ended') {
                // Internship completed (past 60 days) — stop pinging
                if (_timer) {
                    clearInterval(_timer);
                    _timer = null;
                }
            }
        } catch (err) {
            // Silently swallow network errors so user experience is not disrupted
        }
    }

    // Expose globally so portal.html or other scripts can call it
    window.sendAttendancePing = sendAttendancePing;

    // Start background heartbeat: ping every 3 minutes
    _timer = setInterval(sendAttendancePing, PING_INTERVAL_MS);

    // Initial check: if no ping in the last 3 minutes across any tab, ping after a 10s grace period
    setTimeout(() => {
        try {
            const lastPing = parseInt(localStorage.getItem(LOCAL_STORAGE_KEY) || '0', 10);
            if (!lastPing || (Date.now() - lastPing) >= PING_INTERVAL_MS) {
                sendAttendancePing();
            }
        } catch (e) {
            sendAttendancePing();
        }
    }, 10000);
})();
