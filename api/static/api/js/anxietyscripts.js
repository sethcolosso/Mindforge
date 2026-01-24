document.addEventListener('DOMContentLoaded', () => {

    // ─── 1. CONFIGURATION ─────────────────────────────────────────────
    const moodContent = {
        calm: {
            title: "Glad you’re feeling okay. 😌",
            subtitle: "Want to maintain this calm?",
            actions: [
                { text: "Reflect a little", type: "reflect" },
                { text: "Gratitude check", type: "gratitude" },
                { text: "Save this mood", type: "save_mood" }
            ]
        },
        uneasy: {
            title: "Let’s gently slow things down. 🌿",
            subtitle: "What would help right now?",
            actions: [
                { text: "🌱 Ground me", type: "grounding" },
                { text: "💭 Help me reframe", type: "reframe" },
                { text: "📝 Quick reassurance", type: "reassurance" }
            ]
        },
        overwhelmed: {
            title: "That sounds heavy. You don’t have to hold it alone.",
            subtitle: "Let's take one small step.",
            actions: [
                { text: "💬 Let me vent", type: "vent" },
                { text: "🧠 Help me reframe", type: "reframe" },
                { text: "🌿 Ground me", type: "grounding" }
            ]
        },
        panic: {
            title: "You’re safe. Breathe with me.",
            subtitle: "Activate emergency support?",
            actions: [
                { text: "🚨 Start Panic Mode", type: "panic_mode" },
                { text: "📱 Text Safe Person", type: "safe_person" },
                { text: "🚑 Emergency Resources", type: "resources" }
            ]
        }
    };

    // ─── 2. DOM ELEMENTS ──────────────────────────────────────────────
    const moodButtons = document.querySelectorAll('.mood');
    const titleEl = document.getElementById('dynamic-title');
    const subtitleEl = document.getElementById('dynamic-subtitle');
    const actionsContainer = document.getElementById('dynamic-actions');
    const activityArea = document.getElementById('activity-area');
    const activityContent = document.getElementById('activity-content');
    const closeActivityBtn = document.getElementById('close-activity');

    // ─── 3. MOOD SELECTION LOGIC ──────────────────────────────────────
    moodButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Visual toggle
            moodButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Hide previous activity if open
            activityArea.style.display = 'none';

            const moodKey = btn.getAttribute('data-mood');
            const data = moodContent[moodKey];

            if (data) {
                titleEl.textContent = data.title;
                subtitleEl.textContent = data.subtitle;
                actionsContainer.innerHTML = ''; // Clear old buttons

                data.actions.forEach(action => {
                    const newBtn = document.createElement('button');
                    newBtn.className = 'action';
                    newBtn.textContent = action.text;
                    
                    // Panic styling
                    if (moodKey === 'panic') {
                        newBtn.style.borderColor = '#ef4444'; 
                        newBtn.style.color = '#fca5a5';
                    }

                    newBtn.addEventListener('click', () => renderTool(action.type));
                    actionsContainer.appendChild(newBtn);
                });
            }
        });
    });

    closeActivityBtn.addEventListener('click', () => {
        activityArea.style.display = 'none';
    });

    // ─── 4. TOOL RENDERER (The "Why" logic) ───────────────────────────
    function renderTool(type) {
        activityArea.style.display = 'block';
        activityContent.innerHTML = ''; // Clear previous tool
        
        let html = '';

        switch (type) {
            case 'reflect':
            case 'vent':
                html = `
                    <h3>${type === 'vent' ? 'Let it all out 💬' : 'Mini Reflection 📝'}</h3>
                    <p class="muted">${type === 'vent' ? 'Write freely. No judgment.' : 'What went well today?'}</p>
                    <textarea rows="4" placeholder="Type here..."></textarea>
                    <button class="primary" onclick="alert('Entry saved (simulation)')">Save Entry</button>
                `;
                break;

            case 'gratitude':
                html = `
                    <h3>Gratitude Check 🙏</h3>
                    <p class="muted">Name 3 things you're grateful for:</p>
                    <input type="text" placeholder="1. ..." />
                    <input type="text" placeholder="2. ..." />
                    <input type="text" placeholder="3. ..." />
                    <button class="primary" onclick="alert('✨ Wonderful!')">Done</button>
                `;
                break;

            case 'grounding':
                html = `
                    <h3>5-4-3-2-1 Grounding 🌱</h3>
                    <ul class="grounding-list" style="padding:0;">
                        <li>👀 <strong>5</strong> things you see</li>
                        <li>✋ <strong>4</strong> things you touch</li>
                        <li>👂 <strong>3</strong> things you hear</li>
                        <li>👃 <strong>2</strong> things you smell</li>
                        <li>👅 <strong>1</strong> thing you taste</li>
                    </ul>
                    <button class="primary" onclick="alert('Great job grounding your senses.')">Complete</button>
                `;
                break;

            case 'reframe':
                html = `
                    <h3>Cognitive Reframing 🧠</h3>
                    <p><strong>Thought:</strong> "Everyone is judging me."</p>
                    <p class="muted">Challenge it: What specific evidence do I have?</p>
                    <textarea rows="2" placeholder="My reframe: They are probably thinking about themselves..."></textarea>
                    <button class="primary">Save Reframe</button>
                `;
                break;
            
            case 'reassurance':
                html = `
                    <h3>Quick Reassurance 💌</h3>
                    <div style="font-size:1.2rem; margin:20px 0; color:#2dd4bf;">
                         "This feeling is uncomfortable, but it is temporary. You are safe."
                    </div>
                `;
                break;

            case 'panic_mode':
                html = `
                    <h3 style="color:#ef4444">Panic SOS 🛑</h3>
                    <p>Focus on the circle. Inhale as it grows, exhale as it shrinks.</p>
                    <div class="breathing-circle"></div>
                    <p class="muted">You are safe. Keep breathing.</p>
                `;
                activityArea.style.borderColor = '#ef4444';
                break;

            case 'safe_person':
                const msg = encodeURIComponent("I’m feeling panicked right now. Can you check in on me?");
                html = `
                    <h3>Text Safe Person 📱</h3>
                    <p class="muted">We've prepared a message for you.</p>
                    <div style="background:#1f2937; padding:15px; border-radius:8px; margin-bottom:15px;">
                        "I’m feeling panicked right now. Can you check in on me?"
                    </div>
                    <a href="sms:?body=${msg}" class="primary" style="display:inline-block; text-decoration:none;">Open Messages</a>
                `;
                break;

            case 'resources':
                html = `
                    <h3>Emergency Resources 🚑</h3>
                    <ul style="text-align:left; line-height:2;">
                        <li>📞 <strong>988</strong> - Suicide & Crisis Lifeline</li>
                        <li>💬 Text <strong>HOME</strong> to 741741</li>
                        <li>🚑 Call <strong>911</strong> if in immediate danger</li>
                    </ul>
                `;
                break;
                
            case 'save_mood':
                // In a real app, this would be an API call
                alert('Mood saved to your daily log! ✅');
                activityArea.style.display = 'none';
                return; // Early return so we don't show the empty box
        }

        activityContent.innerHTML = html;
        
        // Reset border color if not panic
        if (type !== 'panic_mode') {
            activityArea.style.borderColor = '#2dd4bf';
        }
    }

    // ─── SAFE PERSON LOGIC ─────────────────────────────────────────────
    const btnContactHuman = document.getElementById('btn-contact-human');
    const setupModal = document.getElementById('setup-modal');
    const btnSaveSp = document.getElementById('btn-save-sp');
    const btnCancelSp = document.getElementById('btn-cancel-sp');
    
    // Inputs
    const inputName = document.getElementById('sp-name');
    const inputPhone = document.getElementById('sp-phone');
    const checkDefaultMsg = document.getElementById('sp-default-msg');

    // 1. Handle Main Click
    btnContactHuman.addEventListener('click', () => {
        const savedPerson = localStorage.getItem('mindforge_safe_person');

        if (!savedPerson) {
            // Flow: First time -> Show Setup
            setupModal.style.display = 'flex';
        } else {
            // Flow: Normal -> Execute Contact
            const person = JSON.parse(savedPerson);
            executeContactFlow(person);
        }
    });

    // 2. Save Logic
    btnSaveSp.addEventListener('click', () => {
        const name = inputName.value.trim();
        const phone = inputPhone.value.trim();

        if (!name || !phone) {
            alert("Please enter a name and phone number.");
            return;
        }

        const personData = {
            name: name,
            phone: phone,
            useDefault: checkDefaultMsg.checked
        };

        localStorage.setItem('mindforge_safe_person', JSON.stringify(personData));
        setupModal.style.display = 'none';
        
        // Immediately trigger the flow after saving
        executeContactFlow(personData);
    });

     // 3. Cancel Logic
    btnCancelSp.addEventListener('click', () => {
        setupModal.style.display = 'none';
    });

    // 4. The "Emotional Intelligence" Flow
    function executeContactFlow(person) {
        // Change button text temporarily to provide validation
        const originalText = btnContactHuman.innerText;
        btnContactHuman.innerText = "Reaching out is a strong move... 🤍";
        btnContactHuman.style.background = "#fff";
        btnContactHuman.style.color = "#000";

        const defaultMsg = "Hey, I’m not feeling okay right now. Could you check in on me?";
        const msgBody = person.useDefault ? encodeURIComponent(defaultMsg) : "";
        
        // Small delay so they react to the validation message
        setTimeout(() => {
            window.location.href = `sms:${person.phone}?body=${msgBody}`;
            
            // Reset button after they leave/return
            setTimeout(() => {
                btnContactHuman.innerText = originalText;
                btnContactHuman.style.background = ""; // Reset to CSS default
                btnContactHuman.style.color = "";
            }, 2000);
        }, 1500);
    }

    // 5. Hook into Panic Button (Optional Integration)
    // Modify your existing renderTool switch case for 'panic_mode' to elevate the card
});