document.addEventListener('DOMContentLoaded', () => {
    const instruction = document.getElementById('breath-instruction');
    const timerDisplay = document.getElementById('timer');
    let timeLeft = 15 * 60; // Default 15 mins

    // 1. Sync Text with Breathing Animation (12s total cycle)
    const updateBreathText = () => {
        instruction.textContent = "Inhale...";
        setTimeout(() => instruction.textContent = "Hold...", 4000);
        setTimeout(() => instruction.textContent = "Exhale...", 6000);
    };

    updateBreathText();
    setInterval(updateBreathText, 12000);

    // 2. Countdown Timer
    const countdown = setInterval(() => {
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        timerDisplay.textContent = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        
        if (timeLeft <= 0) {
            clearInterval(countdown);
            alert("Session Complete. Take a moment to notice how you feel.");
            window.location.href = '/exercises/visualization/'; // Updated path
        }
        timeLeft--;
    }, 1000);
});