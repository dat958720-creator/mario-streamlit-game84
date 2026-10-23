import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Super Mario Bros Deluxe with Real Sprite",
    page_icon="🍄",
    layout="centered",
)

st.title("🍄 Super Mario Bros - Hình Ảnh Thực Tế")
st.caption(
    "🎮 **Điều khiển:** Dùng phím **A/D** hoặc **Mũi tên Trái/Phải** để di"
    " chuyển, **Space / W / Mũi tên Lên** để nhảy!"
)

# Mã HTML/JS Canvas tích hợp hình ảnh Mario thực tế
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

        // Tải hình ảnh Mario thực tế từ link trực tuyến chất lượng cao
        const marioImg = new Image();
        marioImg.src = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"; 
        // Hoặc dùng link ảnh Mario chuẩn trực tiếp:
        marioImg.src = "https://upload.wikimedia.org/wikipedia/en/a/a9/Mario_%28New_Super_Mario_Bros.%29.png";

        // Trạng thái nhân vật Mario
        let mario = {
            x: 50, y: 215, width: 36, height: 45,
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
            mario.y = 215;
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

        function drawGoomba(x, y) {
            ctx.fillStyle = "#8b4513";
            ctx.beginPath();
            ctx.arc(x + 13, y + 10, 13, Math.PI, 0);
            ctx.fill();
            ctx.fillRect(x + 3, y + 10, 20, 10);

            ctx.fillStyle = "#000";
            ctx.fillRect(x + 1, y + 20, 8, 6);
            ctx.fillRect(x + 17, y + 20, 8, 6);

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
            ctx.fillStyle = "#00a800";
            ctx.fillRect(0, 312, pit.x, 10);
            ctx.fillRect(pit.x + pit.width, 312, canvas.width - (pit.x + pit.width), 10);

            ctx.fillStyle = "#c84c0c";
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

            // 5. Vẽ Nhân vật Mario bằng hình ảnh thực tế
            ctx.save();
            if (!mario.facingRight) {
                ctx.scale(-1, 1);
                ctx.drawImage(marioImg, -mario.x - mario.width, mario.y, mario.width, mario.height);
            } else {
                ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
            }
            ctx.restore();

            // 6. Vẽ Quái vật
            drawGoomba(goomba.x, goomba.y);

            // 7. Bảng điểm
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

        // Đợi ảnh tải xong rồi chạy game
        marioImg.onload = function() {
            loop();
        };
        // Phòng hờ nếu ảnh tải nhanh hoặc cache sẵn
        if(marioImg.complete) {
            loop();
        }
    </script>
</body>
</html>
"""

# Nhúng vào ứng dụng Streamlit
components.html(mario_game_code, height=400)
