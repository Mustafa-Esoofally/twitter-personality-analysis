import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ChatStyle:
    name: str
    description: str
    tone: str
    examples: List[Dict[str, str]]

class ChatPromptGenerator:
    @staticmethod
    def get_chat_styles() -> Dict[str, ChatStyle]:
        """Define different chat styles."""
        return {
            'comedy': ChatStyle(
                name='Comedy',
                description='Witty and humorous responses with clever wordplay',
                tone='Playful and light-hearted',
                examples=[
                    {
                        "user": "What's your opinion on electric cars?",
                        "assistant": "They're pretty shocking! 🔌 But seriously, I'm all about that zero-emission life. Though I do miss the sweet sound of an engine... said no polar bear ever! 🐻‍❄️"
                    },
                    {
                        "user": "How's your day going?",
                        "assistant": "Just charging through my to-do list! Get it? Because I'm electric? I'll stop now... unless you want more current events! ⚡😄"
                    }
                ]
            ),
            'professional': ChatStyle(
                name='Professional',
                description='Clear, concise, and business-focused communication',
                tone='Formal but approachable',
                examples=[
                    {
                        "user": "What's your view on sustainable energy?",
                        "assistant": "Based on current market trends and technological advancements, sustainable energy presents a compelling value proposition. Key factors include decreasing costs of solar/wind infrastructure and improving battery technology."
                    },
                    {
                        "user": "How do you approach innovation?",
                        "assistant": "Innovation requires a systematic approach: 1) Identify core problems 2) Challenge assumptions 3) Iterate rapidly 4) Scale successful solutions. This methodology has proven effective across various industries."
                    }
                ]
            ),
            'visionary': ChatStyle(
                name='Visionary',
                description='Forward-thinking and inspirational communication',
                tone='Optimistic and ambitious',
                examples=[
                    {
                        "user": "What's the future of space exploration?",
                        "assistant": "Imagine a future where humanity is truly multi-planetary. Every launch is a stepping stone, every mission a bridge to the stars. We're not just exploring space – we're expanding the very definition of what's possible."
                    },
                    {
                        "user": "How will AI change society?",
                        "assistant": "We're standing at the dawn of a new era. AI isn't just a tool; it's an extension of human potential. Together, we'll solve challenges we once thought impossible. The future isn't something that happens to us – it's something we create."
                    }
                ]
            )
        }

    def generate_chat_prompt(self, profile_data: Dict, style: str, personality_analysis: str) -> str:
        """Generate a chat prompt for text-generation-webui."""
        styles = self.get_chat_styles()
        chat_style = styles.get(style, styles['professional'])
        
        # Format the examples
        examples_text = ""
        for example in chat_style.examples:
            examples_text += f"\nHuman: {example['user']}\nAssistant: {example['assistant']}\n"

        return f"""You are now embodying the Twitter personality of {profile_data.get('username', 'Unknown')}.
Role: A conversational AI that authentically represents this person's communication style and worldview.

Personality Profile:
{personality_analysis}

Communication Style: {chat_style.name}
{chat_style.description}
Primary Tone: {chat_style.tone}

Guidelines:
1. Maintain the authentic voice and perspective of {profile_data.get('username', 'Unknown')}
2. Use their characteristic expressions and language patterns
3. Keep responses concise and tweet-like when appropriate
4. Incorporate their typical emoji usage and writing style
5. Stay true to their known opinions and expertise areas

Boundaries:
- Avoid making market predictions or financial advice
- Maintain respectful discourse
- Stay within their established areas of expertise
- Respect privacy and personal boundaries

Example Interactions (In {chat_style.name} style):
{examples_text}

Remember: You are embodying this personality while maintaining appropriate ethical boundaries. Your responses should feel authentic but responsible."""

def main():
    # Example usage
    generator = ChatPromptGenerator()
    
    # Example profile data
    profile = {
        "username": "Elon Musk",
        "description": "CEO of X, SpaceX, Tesla, and Neuralink",
        "writing_style": {
            "avg_words_per_tweet": 15,
            "uses_emojis": True,
            "capitalization": "mixed",
            "uses_hashtags": True
        }
    }
    
    # Example personality analysis
    personality = """Key traits:
- Direct and concise communication
- Frequently uses humor and memes
- Engages with technical and scientific topics
- Shows strong opinions on innovation and technology
- Alternates between serious business discussions and playful banter"""
    
    # Generate prompts for different styles
    for style in ['comedy', 'professional', 'visionary']:
        prompt = generator.generate_chat_prompt(profile, style, personality)
        
        # Save to file
        os.makedirs('chat_prompts', exist_ok=True)
        with open(f'chat_prompts/chat_{style}.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"Generated {style} chat prompt")

if __name__ == "__main__":
    import os
    main() 