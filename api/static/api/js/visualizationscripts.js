document.addEventListener('DOMContentLoaded', () => {
    // 1. Live Duration Update
    const slider = document.getElementById('duration-slider');
    const display = document.getElementById('duration-display');

    slider.addEventListener('input', (e) => {
        const value = e.target.value;
        display.textContent = `${value} minutes`;
        
        // Optional: Add a slight "throb" effect to the text when it changes
        display.style.transform = 'scale(1.1)';
        setTimeout(() => display.style.transform = 'scale(1)', 100);
    });

    // 2. Toggle Voice Selection
    const voiceButtons = document.querySelectorAll('.voice-btn');

    voiceButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            voiceButtons.forEach(b => b.classList.remove('active'));
            // Add active class to the clicked button
            btn.classList.add('active');
        });
    });

    // 3. Start Button Logic
    const startBtn = document.querySelector('.btn-primary-glow');
    startBtn.addEventListener('click', () => {
        const selectedTheme = document.getElementById('theme-select').value;
        const selectedDuration = slider.value;
        const selectedVoice = document.querySelector('.voice-btn.active').textContent;

        console.log(`Starting ${selectedTheme} session for ${selectedDuration} mins with ${selectedVoice} voice.`);
        
        // Add a "loading" state to the button
        startBtn.textContent = "Preparing Sanctuary...";
        startBtn.style.opacity = "0.7";
        
        // Redirect or trigger visualization player after 1.5 seconds
        // Redirect or trigger visualization player after 1.5 seconds
        setTimeout(() => {
            // Replace the alert with the actual redirection
            window.location.href = "/exercises/visualization/player/";
        }, 1500);
    });
});