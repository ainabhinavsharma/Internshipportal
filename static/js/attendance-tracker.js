/**
 * DBERT Global Multi-Page Attendance Tracker
 * Accrues active study and learning time across ALL pages on https://internship.dbert.online/
 * (e.g. Guided Learning, /courses, /courses/<id>/learn, /tasks, /portal, etc.)
 *
 * KEY FEATURES:
 * 1. Persistent Second Accumulator: Active seconds accumulate across page navigations in localStorage.
 *    Navigating every 30-90s across different lessons does NOT reset the timer.
 * 2. Active Presence Detection: Time only counts when the intern is actively interacting (mouse,
 *    scroll, keypress, touch) and the page is visible (not minimized/hidden).
 * 3. Multi-Tab Safe: A shared tick lock ensures having multiple tabs open never inflates or duplicates time.
 * 4. Resilient Heartbeat: When accumulated active time reaches 180s (3 minutes), it pings /attendance/ping
 *    and credits +3 minutes to the intern's weekly attendance.
 */
(function() {
    'use strict';

    if (window.__dbertAttendanceTrackerInstalled) return;
    window.__dbertAttendanceTrackerInstalled = true;

    const TARGET_ACTIVE_SEC = 180; // 3 minutes = 180 active seconds
    const KEY_ACTIVE_SEC = 'dbert_att_active_sec';
    const KEY_LAST_TICK = 'dbert_att_last_tick_ms';
    const KEY_LAST_PING = 'dbert_att_last_ping_ms';
    const KEY_LAST_USER_ACT = 'dbert_att_user_act_ms';
    const IDLE_TIMEOUT_MS = 120000; // 2 minutes without user interaction pauses active accrual

    let _lastLocalActivity = Date.now();
    let _isPinging = false;
    let _accrualTimer = null;

    // Track user interaction (mouse, touch, keyboard, scroll) to ensure active presence
    function markUserActive() {
        _lastLocalActivity = Date.now();
        try {
            localStorage.setItem(KEY_LAST_USER_ACT, _lastLocalActivity.toString());
        } catch (e) {}
    }

    const activityEvents = ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
    activityEvents.forEach(evt => {
        window.addEventListener(evt, markUserActive, { passive: true });
    });

    // Check if the intern is actively looking at / interacting with this tab
    function isInternActive() {
        if (document.hidden) return false;
        const now = Date.now();
        let lastAct = _lastLocalActivity;
        try {
            const stored = parseInt(localStorage.getItem(KEY_LAST_USER_ACT) || '0', 10);
            if (stored > lastAct) lastAct = stored;
        } catch (e) {}
        return (now - lastAct) < IDLE_TIMEOUT_MS;
    }

    // Ping the server to credit +3 minutes
    async function sendAttendancePing() {
        if (_isPinging) return;
        _isPinging = true;

        try {
            // Prevent duplicate server calls if another tab just pinged in the last 110s
            const lastPing = parseInt(localStorage.getItem(KEY_LAST_PING) || '0', 10);
            const now = Date.now();
            if (now - lastPing < 110000) {
                _isPinging = false;
                return;
            }

            // Retrieve CSRF token if meta tag exists
            const meta = document.querySelector('meta[name="csrf-token"]');
            const csrfToken = meta ? meta.getAttribute('content') : '';

            const headers = { 'Content-Type': 'application/json' };
            if (csrfToken) {
                headers['X-CSRF-Token'] = csrfToken;
            }

            const res = await fetch('/attendance/ping', {
                method: 'POST',
                credentials: 'include',
                headers: headers
            });

            if (res.status === 401) {
                // Not logged in — stop accruing on this session
                if (_accrualTimer) {
                    clearInterval(_accrualTimer);
                    _accrualTimer = null;
                }
                _isPinging = false;
                return;
            }

            if (!res.ok) {
                _isPinging = false;
                return;
            }

            const data = await res.json();
            if (data.status === 'success') {
                localStorage.setItem(KEY_LAST_PING, Date.now().toString());

                // Deduct 180s from accumulated active seconds
                let currentSec = parseInt(localStorage.getItem(KEY_ACTIVE_SEC) || '0', 10);
                if (isNaN(currentSec)) currentSec = 0;
                currentSec = Math.max(0, currentSec - TARGET_ACTIVE_SEC);
                localStorage.setItem(KEY_ACTIVE_SEC, currentSec.toString());

                // If on portal dashboard, update the live attendance counter immediately
                if (typeof window.updateLiveCounter === 'function') {
                    window.updateLiveCounter(data.total_minutes);
                }

                // Broadcast sync event to any other open tabs
                window.dispatchEvent(new CustomEvent('dbert_attendance_synced', { detail: data }));
            } else if (data.reason === 'internship_ended') {
                if (_accrualTimer) {
                    clearInterval(_accrualTimer);
                    _accrualTimer = null;
                }
            }
        } catch (err) {
            // Network failure will retry on next cycle
        } finally {
            _isPinging = false;
        }
    }

    // Second-by-second accumulator: increments active study time in localStorage
    function tick() {
        if (!isInternActive()) return;

        const now = Date.now();
        try {
            // Multi-tab arbitration: only one tab ticks per 850ms window
            const lastTick = parseInt(localStorage.getItem(KEY_LAST_TICK) || '0', 10);
            if (now - lastTick < 850) {
                return;
            }
            localStorage.setItem(KEY_LAST_TICK, now.toString());

            let sec = parseInt(localStorage.getItem(KEY_ACTIVE_SEC) || '0', 10);
            if (isNaN(sec) || sec < 0) sec = 0;
            sec += 1;
            localStorage.setItem(KEY_ACTIVE_SEC, sec.toString());

            // When accumulated active seconds reach 180s (3 minutes), trigger server ping
            if (sec >= TARGET_ACTIVE_SEC) {
                sendAttendancePing();
            }
        } catch (e) {}
    }

    // Expose sendAttendancePing globally for portal.html compatibility
    window.sendAttendancePing = sendAttendancePing;

    // Start 1-second active accrual heartbeat
    _accrualTimer = setInterval(tick, 1000);

    // Initial check on page load: if prior pages already accumulated >= 180s, ping immediately!
    function checkPendingPing() {
        try {
            const sec = parseInt(localStorage.getItem(KEY_ACTIVE_SEC) || '0', 10);
            if (sec >= TARGET_ACTIVE_SEC) {
                sendAttendancePing();
            }
        } catch (e) {}
    }

    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            markUserActive();
            checkPendingPing();
        }
    });

    window.addEventListener('beforeunload', () => {
        try {
            localStorage.setItem(KEY_LAST_TICK, Date.now().toString());
        } catch (e) {}
    });

    // Cross-tab sync: if another tab completed a ping, refresh this tab's portal view if open
    window.addEventListener('storage', (e) => {
        if (e.key === KEY_LAST_PING) {
            if (typeof window.loadAttendance === 'function') {
                window.loadAttendance();
            }
        }
    });

    // Run initial check after 2 seconds on page load
    setTimeout(checkPendingPing, 2000);
})();
