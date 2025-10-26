        
        // all the current expressions
        const EXPRESSIONS = ["sad","happy","confused","mad","freaky","relaxed","shocked"];
        // map model outputs -> your 7 UI buckets
        const LABEL_MAP = {
        sad:"sad", happy:"happy", confused:"confused" , mad:"mad",
        freaky:"freaky", relaxed:"relaxed", surprised:"shocked"
        };
        
        // Navigation state management
        const navLinks = document.querySelectorAll('.nav-opts a');
        const sections = document.querySelectorAll('.section');

        // Function to update active nav link
        function updateActiveNav() {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;1
                if (window.scrollY >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });

            navOpts.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        }

            
        // simple default image paths (drop files in photos/expressions/*.png)
        const IMG = Object.fromEntries(EXPRESSIONS.map(n => [n, `photos/expressions/${n}.png`]));

        // ----- minimal UI wiring -----
        const startBtn = document.getElementById("startBtn");
        const guidelinesCard = document.getElementById("guidelinesCard"); // if you have it
        const videoEl = document.getElementById("camera");
        const canvas = document.getElementById("offscreen");
        const ctx = canvas.getContext("2d");
        const expressionImage = document.getElementById("expressionImage");
        const expressionLabel = document.getElementById("expressionLabel");

        // send ~5 fps small jpegs
        const W = 320, H = 240, FPS_MS = 200;
        let stream=null, timer=null;
        const socket = io(); // default connect to same origin

        function fadeGuidelines(){ guidelinesCard?.classList.add("fade-out"); }

        async function startCamera(){
        stream = await navigator.mediaDevices.getUserMedia({ video:{facingMode:"user"}, audio:false });
        videoEl.srcObject = stream; await videoEl.play();
        canvas.width = W; canvas.height = H;
        socket.emit("start", {ts: Date.now()});
        timer = setInterval(()=>{
            if (!videoEl.videoWidth) return;
            ctx.drawImage(videoEl, 0, 0, W, H);
            const jpeg = canvas.toDataURL("image/jpeg", 0.65);
            socket.emit("frame", { image: jpeg });
        }, FPS_MS);
        }

        socket.on("expression", ({expression, score})=>{
        const raw = (expression||"").toLowerCase();
        const key = LABEL_MAP[raw] || "relaxed";
        expressionImage.src = IMG[key];
        expressionLabel.textContent = `${key[0].toUpperCase()+key.slice(1)}${Number.isFinite(score)?` (${score.toFixed(2)})`:''}`;
        });

        startBtn?.addEventListener("click", async ()=>{
        fadeGuidelines();
        try { await startCamera(); } catch(e){ alert("Allow camera access to continue."); }
        });


        // waits for scroll events
        window.addEventListener('scroll', updateActiveNav);