import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Super Mario Bros Deluxe", page_icon="🍄", layout="centered"
)

st.title("🍄 Super Mario Bros - Deluxe Edition")
st.caption(
    "🎮 **Điều khiển:** Dùng phím **A/D** hoặc **Mũi tên Trái/Phải** để di"
    " chuyển, **Space / W / Mũi tên Lên** để nhảy!"
)

# Mã HTML/JS Canvas Nâng Cấp Đồ Họa & Bảng Game Over
mario_game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; padding: 0; background: #0e1117; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #game-container { position: relative; width: 640px; height: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); border-radius: 12px; overflow: hidden; border: 3px solid #333; }
        canvas { background: linear-gradient(to bottom, #5c94fc 0%, #8daee8 80%, #c1d7ff 100%); display: block; }
        
        /* Modal Popup Game Over */
        #game-over-screen {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(4px);
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            z-index: 10;
            animation: fadeIn 0.3s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }

        .go-box {
            background: #1e222a;
            border: 3px solid #ff4b4b;
            border-radius: 16px;
            padding: 25px 40px;
            text-align: center;
            box-shadow: 0 0 25px rgba(255, 75, 75, 0.4);
        }

        .go-title {
            font-size: 42px;
            font-weight: 900;
            color: #ff4b4b;
            text-shadow: 3px 3px 0px #800000;
            margin: 0 0 10px 0;
            letter-spacing: 2px;
        }

        .go-desc {
            font-size: 16px;
            color: #ddd;
            margin-bottom: 20px;
        }

        .restart-btn {
            background: linear-gradient(135deg, #ff4b4b, #ff2222);
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3);
            transition: all 0.2s ease;
        }

        .restart-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 75, 75, 0.5);
            background: linear-gradient(135deg, #ff6b6b, #ff3333);
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="640" height="380"></canvas>
        
        <!-- Bảng Game Over -->
        <div id="game-over-screen">
            <div class="go-box">
                <div style="font-size: 48px; margin-bottom: 5px;">👾 💥</div>
                <div class="go-title">GAME OVER</div>
                <div class="go-desc">Bạn đã va chạm phải quái vật hoặc rơi xuống hố!</div>
                <button class="restart-btn" onclick="resetGame()">🔄 CHƠI LẠI</button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const gameOverScreen = document.getElementById("game-over-screen");

        let isGameOver = false;
        let score = 0;

        // Trạng thái nhân vật Mario
        let mario = {
            x: 50, y: 220, width: 28, height: 36,
            dx: 0, dy: 0, speed: 4.5, gravity: 0.45,
            jumpPower: -10, grounded: false, facingRight: true
        };

        // Kẻ địch Goomba
        let goomba = {
            x: 400, y: 286, width: 26, height: 26,
            speed: 1.5, dir: -1
        };

        // Khối hố nguy hiểm trên đường
        let pit = { x: 280, width: 70 };

        // Vật phẩm Đồng xu & Khối hỏi chấm
        let coins = [
            { x: 180, y: 190, size: 14, collected: false },
            { x: 220, y: 190, size: 14, collected: false },
            { x: 480, y: 220, size: 14, collected: false }
        ];

        let keys = {};

        document.addEventListener("keydown", (e) => { keys[e.code] = true; });
        document.addEventListener("keyup", (e) => { keys[e.code] = false; });

        function resetGame() {
            mario.x = 50;
            mario.y = 220;
            mario.dy = 0;
            goomba.x = 400;
            goomba.dir = -1;
            score = 0;
            coins.forEach(c => c.collected = false);
            isGameOver = false;
            gameOverScreen.style.display = "none";
            loop();
        }

        function update() {
            if (isGameOver) return;

            // Xử lý di chuyển
            if (keys["ArrowRight"] || keys["KeyD"]) {
                mario.x += mario.speed;
                mario.facingRight = true;
            }
            if (keys["ArrowLeft"] || keys["KeyA"]) {
                mario.x -= mario.speed;
                mario.facingRight = false;
            }

            // Nhảy
            if ((keys["Space"] || keys["ArrowUp"] || keys["KeyW"]) && mario.grounded) {
                mario.dy = mario.jumpPower;
                mario.grounded = false;
            }

            // Trọng lực
            mario.dy += mario.gravity;
            mario.y += mario.dy;

            // Giới hạn biên trái/phải
            if (mario.x < 0) mario.x = 0;
            if (mario.x + mario.width > canvas.width) mario.x = canvas.width - mario.width;

            // Kiểm tra đứng trên mặt đất (Độ cao đất: y = 312)
            const groundY = 312;
            const overPit = (mario.x + mario.width > pit.x && mario.x < pit.x + pit.width);

            if (mario.y + mario.height >= groundY) {
                if (overPit) {
                    // Rơi xuống hố
                    if (mario.y > canvas.height) {
                        triggerGameOver();
                    }
                } else {
                    mario.y = groundY - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }
            }

            // Cập nhật quái vật Goomba
            goomba.x += goomba.speed * goomba.dir;
            if (goomba.x <= 360 || goomba.x >= 580) goomba.dir *= -1;

            // Va chạm giữa Mario và Goomba
            if (
                mario.x < goomba.x + goomba.width &&
                mario.x + mario.width > goomba.x &&
                mario.y < goomba.y + goomba.height &&
                mario.y + mario.height > goomba.y
            ) {
                triggerGameOver();
            }

            // Ăn xu
            coins.forEach(c => {
                if (!c.collected &&
                    mario.x < c.x + c.size &&
                    mario.x + mario.width > c.x &&
                    mario.y < c.y + c.size &&
                    mario.y + mario.height > c.y) {
                    c.collected = true;
                    score += 100;
                }
            });
        }

        function triggerGameOver() {
            isGameOver = true;
            gameOverScreen.style.display = "flex";
        }

        /* --- VẼ ĐỒ HOẠ GAME CHẤT LƯỢNG CAO --- */
        function drawMario(x, y, facingRight) {
            ctx.save();
            // Nón đỏ
            ctx.fillStyle = "#e52521";
            ctx.fillRect(x + 4, y, 20, 8);
            ctx.fillRect(x + 8, y - 4, 12, 4);

            // Khuôn mặt
            ctx.fillStyle = "#fcc082";
            ctx.fillRect(x + 4, y + 8, 20, 10);
            
            // Mắt & Râu
            ctx.fillStyle = "#000";
            const eyeX = facingRight ? x + 18 : x + 6;
            ctx.fillRect(eyeX, y + 10, 3, 4);
            ctx.fillRect(x + 4, y + 15, 20, 3); // Râu

            // Áo đỏ
            ctx.fillStyle = "#e52521";
            ctx.fillRect(x + 4, y + 18, 20, 8);

            // Quần yếm xanh dương
            ctx.fillStyle = "#002490";
            ctx.fillRect(x + 6, y + 22, 16, 10);
            
            // Khuy quần vàng
            ctx.fillStyle = "#fbd000";
            ctx.fillRect(x + 8, y + 24, 3, 3);
            ctx.fillRect(x + 17, y + 24, 3, 3);

            // Giày nâu
            ctx.fillStyle = "#8b4513";
            ctx.fillRect(x + 2, y + 32, 11, 4);
            ctx.fillRect(x + 15, y + 32, 11, 4);
            ctx.restore();
        }

        function drawGoomba(x, y) {
            // Nấm Goomba Nâu
            ctx.fillStyle = "#8b4513";
            ctx.beginPath();
            ctx.arc(x + 13, y + 10, 13, Math.PI, 0);
            ctx.fill();
            ctx.fillRect(x + 3, y + 10, 20, 10);

            // Chân
            ctx.fillStyle = "#000";
            ctx.fillRect(x + 1, y + 20, 8, 6);
            ctx.fillRect(x + 17, y + 20, 8, 6);

            // Mắt
            ctx.fillStyle = "#fff";
            ctx.fillRect(x + 5, y + 8, 5, 8);
            ctx.fillRect(x + 16, y + 8, 5, 8);
            ctx.fillStyle = "#000";
            ctx.fillRect(x + 7, y + 10, 3, 5);
            ctx.fillRect(x + 16, y + 10, 3, 5);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ Đám Mây
            ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
            ctx.beginPath(); ctx.arc(100, 60, 20, 0, Math.PI * 2); ctx.arc(125, 50, 28, 0, Math.PI * 2); ctx.arc(150, 60, 20, 0, Math.PI * 2); ctx.fill();
            ctx.beginPath(); ctx.arc(450, 80, 22, 0, Math.PI * 2); ctx.arc(480, 70, 30, 0, Math.PI * 2); ctx.arc(510, 80, 22, 0, Math.PI * 2); ctx.fill();

            // 2. Vẽ Khối 🧱 & ❓
            ctx.fillStyle = "#fbd000";
            ctx.fillRect(180, 220, 26, 26); ctx.strokeRect(180, 220, 26, 26);
            ctx.fillStyle = "#000"; ctx.font = "bold 16px sans-serif"; ctx.fillText("?", 188, 240);

            // 3. Vẽ Mặt đất & Hố
            ctx.fillStyle = "#00a800"; // Lớp cỏ xanh
            ctx.fillRect(0, 312, pit.x, 10);
            ctx.fillRect(pit.x + pit.width, 312, canvas.width - (pit.x + pit.width), 10);

            ctx.fillStyle = "#c84c0c"; // Đất nâu
            ctx.fillRect(0, 322, pit.x, 58);
            ctx.fillRect(pit.x + pit.width, 322, canvas.width - (pit.x + pit.width), 58);

            // 4. Vẽ Vật phẩm Xu
            coins.forEach(c => {
                if (!c.collected) {
                    ctx.fillStyle = "#fbd000";
                    ctx.beginPath();
                    ctx.arc(c.x, c.y, c.size / 2, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = "#d4a000";
                    ctx.stroke();
                }
            });

            // 5. Vẽ Nhân vật & Quái vật
            drawMario(mario.x, mario.y, mario.facingRight);
            drawGoomba(goomba.x, goomba.y);

            // 6. Bảng điểm
            ctx.fillStyle = "#fff";
            ctx.font = "bold 16px 'Segoe UI', sans-serif";
            ctx.fillText("💰 ĐIỂM: " + score, 20, 35);
        }

        function loop() {
            update();
            draw();
            if (!isGameOver) {
                requestAnimationFrame(loop);
            }
        }

        loop();
    </script>
</body>
</html>
"""

# Nhúng vào ứng dụng Streamlit
components.html(mario_game_code, height=400)
