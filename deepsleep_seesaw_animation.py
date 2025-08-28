import base64

# --- User Inputs ---
# Update these file paths to match your image names
GOOD_SLEEP_IMAGE = "./img/good_sleep_emoji.png"
LOW_SLEEP_IMAGE = "./img/low_sleep_emoji.png"

# Update these values to test different scenarios
good_count = 4
low_count = 6
initial_emoji_size = 60
final_size_change = 1.30 # 30% increase/decrease

# --- Helper function to encode image to Base64 ---
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# --- Generate the HTML content ---
def generate_animated_html(good_count, low_count):
    # Encode images to Base64 to embed them directly in the HTML
    good_emoji_base64 = get_image_base64(GOOD_SLEEP_IMAGE)
    low_emoji_base64 = get_image_base64(LOW_SLEEP_IMAGE)

    # Calculate final animation values
    total_count = good_count + low_count
    tilt_degrees = 0
    low_size_factor = 1.0 # Factor to multiply initial_emoji_size by
    good_size_factor = 1.0 # Factor to multiply initial_emoji_size by

    if total_count > 0:
        good_percent = good_count / total_count
        low_percent = low_count / total_count
        
        # Calculate tilt angle (e.g., up to 20 degrees)
        tilt_degrees = (good_percent - low_percent) * 20

        # Calculate emoji size factors
        if good_count > low_count:
            good_size_factor = final_size_change
            low_size_factor = 1 / final_size_change
        elif low_count > good_count:
            good_size_factor = 1 / final_size_change
            low_size_factor = final_size_change
    
    # Generate the HTML, CSS, and JavaScript
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: white;
            overflow: hidden;
        }}
        .container {{
            position: relative;
            width: 800px;
            height: 400px;
        }}
        .seesaw-pivot-container {{
            position: absolute;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
        }}
        .pivot-block {{
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 50px;
            height: 40px;
            background-color: black;
            transform: translateX(-50%);
            border-radius: 10px;
            z-index: 1;
        }}
        .seesaw-bar {{
            position: relative;
            width: 400px;
            height: 5px;
            background-color: black;
            transform-origin: center;
            transition: transform 1s ease-in-out;
            transform: rotate(0deg);
            z-index: 2;
            bottom: 40px;
        }}
        .emoji-wrapper {{
            position: absolute;
            bottom: -25px;
            transition: all 1s ease-in-out;
            transform-origin: 50% 100%;
            /* Set a base size for the wrapper and let transforms handle scaling */
            width: {initial_emoji_size}px;
            height: {initial_emoji_size}px;
        }}
        #low-wrapper {{
            left: -30px;
        }}
        #good-wrapper {{
            right: -30px;
        }}
        .emoji {{
            width: 100%; /* The emoji fills the wrapper */
            height: 100%; /* The emoji fills the wrapper */
            border-radius: 30%;
            object-fit: cover;
        }}
        .counter {{
            position: absolute;
            top: 0px;
            right: 0px;
            width: 25px;
            height: 25px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: sans-serif;
            font-size: 12px;
            font-weight: bold;
            color: black;
            border-radius: 50%;
            border-style: double;
            border-width: 3px;
            background-color: white;
            z-index: 3;
            /* Use translate to create the overlap */
            transform: translate(50%, -50%);
        }}
        .good-counter {{
            border-color: green;
        }}
        .low-counter {{
            border-color: red;
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="seesaw-pivot-container">
            <div class="pivot-block"></div> 
            <div class="seesaw-bar" id="seesaw-bar">
                <div class="emoji-wrapper" id="low-wrapper">
                    <img id="low-emoji" class="emoji" src="data:image/png;base64,{low_emoji_base64}">
                    <div class="counter low-counter">{low_count}</div>
                </div>
                <div class="emoji-wrapper" id="good-wrapper">
                    <img id="good-emoji" class="emoji" src="data:image/png;base64,{good_emoji_base64}">
                    <div class="counter good-counter">{good_count}</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const finalTilt = {tilt_degrees};
        const lowSizeFactor = {low_size_factor};
        const goodSizeFactor = {good_size_factor};

        const seesawBar = document.getElementById('seesaw-bar');
        const lowWrapper = document.getElementById('low-wrapper');
        const goodWrapper = document.getElementById('good-wrapper');

        // Trigger the animation after a short delay to allow initial rendering
        setTimeout(() => {{
            // Animate the seesaw tilt
            seesawBar.style.transform = `rotate(${{finalTilt}}deg)`;

            // Combine transforms for both rotation and scaling on the wrapper
            lowWrapper.style.transform = `rotate(${{-finalTilt}}deg) scale(${{lowSizeFactor}})`;
            goodWrapper.style.transform = `rotate(${{-finalTilt}}deg) scale(${{goodSizeFactor}})`;

        }}, 50);
    </script>
    </body>
    </html>
    """
    return html_content

# Generate the HTML file
html_output = generate_animated_html(good_count, low_count)
with open("animated_seesaw.html", "w") as file:
    file.write(html_output)

print("✅ Animated see-saw HTML file generated successfully as animated_seesaw.html")
print("Open this file in your browser to see the animation.")