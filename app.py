import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Load security environment variables
load_dotenv()

# 2. Correctly initialize Flask pointing to your lowercase templates folder
app = Flask(__name__, template_folder='templates')

# Initialize the Groq Client safely using the key from your .env file
# Replace everything on line 12 with your real key directly:
groq_client = Groq(api_key="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")

@app.route('/')
def index():
    # Renders the main user dashboard UI
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    description = data.get('description', '')
    platform = data.get('platform', 'Instagram')
    tone = data.get('tone', 'Casual')

    # Constructing a structured prompt to guide the LLaMA 3.3 model outputs
    system_prompt = (
        "You are an expert social media AI assistant. Your task is to output exactly three parts "
        "based on user input: 3 optimized captions, 10 relevant hashtags (mix of popular and niche), "
        "and 3 punchy Call-to-Actions (CTAs).\n"
        "Format your entire response cleanly so it is easy to read."
    )
    
    user_prompt = f"Platform: {platform}\nTone: {tone}\nDescription of Post: {description}"

    try:
        # Requesting generation from the LLaMA 3.3 model via Groq API
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        ai_response = completion.choices[0].message.content
        return jsonify({"success": True, "result": ai_response})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)