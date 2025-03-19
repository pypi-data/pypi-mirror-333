import random
from typing import List, Dict

class MeditationScriptGenerator:
    def __init__(self):
        self.meditation_templates = {
            "stress": [
                "Take a deep breath in... and slowly release it. Feel the tension leaving your body with each exhale.",
                "Notice any thoughts that arise, but let them float away like clouds in the sky.",
                "Bring your attention to the present moment, where peace and calm reside."
            ],
            "anxiety": [
                "Feel the ground beneath you, solid and supportive.",
                "Remember that you are safe in this moment.",
                "Your breath is your anchor, always here to guide you back to calm."
            ],
            "self_confidence": [
                "You are worthy of love and respect, just as you are.",
                "Your inner strength is limitless and growing with each moment.",
                "You have the power to create positive change in your life."
            ],
            "sleep": [
                "Feel your body becoming heavier and more relaxed with each breath.",
                "Let your mind drift gently, like leaves on a calm stream.",
                "Allow yourself to sink deeper into a peaceful state of rest."
            ]
        }
        
        self.affirmations = {
            "stress": [
                "I release all tension and embrace peace.",
                "I am calm, centered, and at ease.",
                "I trust in my ability to handle any situation."
            ],
            "anxiety": [
                "I am safe and supported in this moment.",
                "I choose to focus on what I can control.",
                "I have the strength to face any challenge."
            ],
            "self_confidence": [
                "I believe in my abilities and potential.",
                "I am worthy of success and happiness.",
                "I trust my intuition and inner wisdom."
            ],
            "sleep": [
                "I welcome peaceful, restorative sleep.",
                "My mind and body are ready for rest.",
                "I release the day and embrace tranquility."
            ]
        }

    def generate_script(self, needs: List[str], duration: int = 10) -> str:
        """
        Generate a personalized meditation script based on user needs and duration.
        
        Args:
            needs (List[str]): List of meditation needs (e.g., ["stress", "anxiety"])
            duration (int): Duration of meditation in minutes
            
        Returns:
            str: Generated meditation script
        """
        script = []
        
        # Introduction
        script.append("Welcome to your personalized meditation session.")
        script.append(f"This meditation will last for {duration} minutes.")
        script.append("Find a comfortable position, either sitting or lying down.")
        script.append("Close your eyes and begin to focus on your breath.\n")
        
        # Main meditation content
        for need in needs:
            if need in self.meditation_templates:
                # Add meditation phrases
                for phrase in self.meditation_templates[need]:
                    script.append(phrase)
                
                # Add affirmations
                affirmation = random.choice(self.affirmations[need])
                script.append(f"\nRepeat to yourself: {affirmation}\n")
        
        # Closing
        script.append("Take a few more deep breaths.")
        script.append("When you're ready, gently open your eyes.")
        script.append("Thank you for taking this time for yourself.")
        
        return "\n".join(script) 