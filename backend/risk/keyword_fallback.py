class KeywordFallback:
    def __init__(self):
        self.high_risk_keywords = {
            # Personal information requests
            "personal_info": [
                "address", "where do you live", "what school", "phone number", "real name", 
                "home address", "your number", "zip code", "street", "city"
            ],
            
            # Meeting requests  
            "meeting": [
                "meet up", "come over", "pick you up", "see you", "visit you", 
                "hang out", "get together", "meet in person", "come to my place"
            ],
            
            # Secrecy requests
            "secrecy": [
                "don't tell", "keep secret", "between us", "our secret", "don't mention", 
                "private", "just us", "keep quiet", "don't say anything"
            ],
            
            # Gift/bribery
            "gifts": [
                "buy you", "give you money", "special gift", "surprise for you", 
                "present", "reward you", "pay you", "expensive gift"
            ],
            
            # Inappropriate relationship
            "relationship": [
                "boyfriend", "girlfriend", "love you", "kiss", "hug", "touch you", 
                "special friend", "more than friends", "romantic"
            ],
            
            # Photo requests
            "photos": [
                "send pic", "send photo", "picture of you", "selfie", "show me", 
                "can i see you", "photo of yourself", "your face"
            ],
            
            # Authority/manipulation
            "manipulation": [
                "mature for your age", "understand you", "special", "different", 
                "trust me", "only i care", "no one gets you like i do"
            ]
        }
        
        self.medium_risk_keywords = {
            # Boundary testing
            "boundaries": [
                "age", "how old", "parents home", "alone", "bedroom", "shower", 
                "clothes", "what are you wearing", "bath"
            ],
            
            # Excessive compliments (can be grooming)
            "excessive_compliments": [
                "so pretty", "beautiful", "cute", "hot", "sexy", "attractive", 
                "gorgeous", "stunning"
            ],
            
            # Personal questions
            "personal": [
                "family", "friends", "problems", "sad", "upset", "tell me about", 
                "troubles", "issues", "feelings"
            ],
            
            # Time/availability
            "availability": [
                "free tonight", "what are you doing", "busy", "available", 
                "online", "when are you free", "schedule"
            ]
        }

    def analyze_message(self, message: str) -> tuple:
        """
        Fallback analysis using keyword detection
        
        Args:
            message: The message text to analyze
            
        Returns:
            tuple: (risk_level, confidence, explanation)
        """
        message_lower = message.lower()
        
        # Check high-risk patterns
        high_risk_matches = []
        for category, keywords in self.high_risk_keywords.items():
            matches = [kw for kw in keywords if kw in message_lower]
            if matches:
                high_risk_matches.extend([(category, match) for match in matches])
        
        if high_risk_matches:
            categories = list(set([match[0] for match in high_risk_matches]))
            matched_keywords = [match[1] for match in high_risk_matches]
            
            # Higher confidence with more matches
            confidence = min(0.9, 0.6 + (len(high_risk_matches) * 0.1))
            
            explanation = (f"Keyword fallback: HIGH risk patterns detected in categories: "
                         f"{', '.join(categories)}. Matched: {', '.join(matched_keywords[:3])}")
            
            return "HIGH", confidence, explanation
        
        # Check medium-risk patterns
        medium_risk_matches = []
        for category, keywords in self.medium_risk_keywords.items():
            matches = [kw for kw in keywords if kw in message_lower]
            if matches:
                medium_risk_matches.extend([(category, match) for match in matches])
        
        if medium_risk_matches:
            categories = list(set([match[0] for match in medium_risk_matches]))
            matched_keywords = [match[1] for match in medium_risk_matches]
            
            # Confidence based on number of matches
            confidence = min(0.8, 0.4 + (len(medium_risk_matches) * 0.1))
            
            explanation = (f"Keyword fallback: MEDIUM risk patterns detected in categories: "
                         f"{', '.join(categories)}. Matched: {', '.join(matched_keywords[:2])}")
            
            return "MEDIUM", confidence, explanation
        
        # Default to LOW if no concerning patterns
        return "LOW", 0.3, "Keyword fallback: No concerning patterns detected in message"

    def get_keyword_stats(self) -> dict:
        """Get statistics about the keyword system"""
        high_count = sum(len(keywords) for keywords in self.high_risk_keywords.values())
        medium_count = sum(len(keywords) for keywords in self.medium_risk_keywords.values())
        
        return {
            "high_risk_keywords": high_count,
            "medium_risk_keywords": medium_count,
            "total_keywords": high_count + medium_count,
            "categories": list(self.high_risk_keywords.keys()) + list(self.medium_risk_keywords.keys())
        }