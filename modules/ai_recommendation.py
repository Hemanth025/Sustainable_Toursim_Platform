"""
AI Recommendation Module
Implements Content-Based Filtering using TF-IDF and Cosine Similarity.
Designed to run with minimal dependencies (numpy optional but preferred, standard lib fallback).
"""

import math
import re
from collections import Counter

class AIRecommender:
    def __init__(self, destinations_data):
        """
        Initialize the recommender with destination data.
        destinations_data: Dictionary of destination objects
        """
        self.destinations = destinations_data
        self.corpus = []
        self.doc_ids = []
        self.idf = {}
        self.tf_vectors = {}
        self.doc_norms = {}
        
        # Build corpus and train
        self._prepare_corpus()
        self._compute_tfidf()

    def _tokenize(self, text):
        """Simple tokenizer: lowercase, remove special chars, split"""
        text = text.lower()
        # Remove non-alphanumeric chars
        text = re.sub(r'[^a-z0-9\s]', '', text)
        words = text.split()
        # Basic stop words removal
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        return [w for w in words if w not in stop_words]

    def _prepare_corpus(self):
        """Convert destination features into a text corpus"""
        for dest_id, data in self.destinations.items():
            # Combine relevant fields for content matching
            # Weighting: Name (2x), Type (2x), Features (1.5x), Description (1x)
            
            text_parts = []
            
            # Name
            text_parts.extend([data['name']] * 2)
            
            # Types
            if isinstance(data.get('type'), list):
                text_parts.extend(data['type'] * 2)
            
            # Sustainability features
            if isinstance(data.get('sustainability_features'), list):
                text_parts.extend(data['sustainability_features'])
                
            # Description
            text_parts.append(data.get('description', ''))
            
            # Join and tokenize
            full_text = " ".join(text_parts)
            self.corpus.append(full_text)
            self.doc_ids.append(dest_id)

    def _compute_tfidf(self):
        """Compute TF-IDF vectors for the corpus"""
        N = len(self.corpus)
        df = Counter()
        
        # 1. Calculate DF (Document Frequency)
        doc_vocabs = []
        for doc in self.corpus:
            tokens = set(self._tokenize(doc))
            doc_vocabs.append(tokens)
            df.update(tokens)
            
        # 2. Calculate IDF
        self.idf = {term: math.log(1 + N / (count + 1)) for term, count in df.items()}
        
        # 3. Calculate TF-IDF Vectors
        for i, doc_text in enumerate(self.corpus):
            tokens = self._tokenize(doc_text)
            term_counts = Counter(tokens)
            total_terms = len(tokens) if tokens else 1
            
            # TF: Term Count / Total Terms in Doc
            # Vector is a dict {term: score}
            vec = {}
            for term, count in term_counts.items():
                tf = count / total_terms
                vec[term] = tf * self.idf.get(term, 0)
                
            self.tf_vectors[self.doc_ids[i]] = vec
            
            # Precompute norm for cosine similarity
            norm_sq = sum(score ** 2 for score in vec.values())
            self.doc_norms[self.doc_ids[i]] = math.sqrt(norm_sq)

    def _vectorize_query(self, query):
        """Convert a user query into a TF-IDF vector"""
        tokens = self._tokenize(query)
        term_counts = Counter(tokens)
        total_terms = len(tokens) if tokens else 1
        
        vec = {}
        for term, count in term_counts.items():
            if term in self.idf:
                tf = count / total_terms
                vec[term] = tf * self.idf[term]
        
        return vec

    def recommend(self, query, top_k=3):
        """
        Recommend destinations based on query using Cosine Similarity
        """
        query_vec = self._vectorize_query(query)
        query_norm = math.sqrt(sum(score ** 2 for score in query_vec.values()))
        
        if query_norm == 0:
            return []
            
        scores = []
        
        for dest_id, dest_vec in self.tf_vectors.items():
            # Dot product
            dot_product = 0
            for term, q_score in query_vec.items():
                if term in dest_vec:
                    dot_product += q_score * dest_vec[term]
            
            # Cosine Similarity = (A . B) / (||A|| * ||B||)
            dest_norm = self.doc_norms[dest_id]
            
            if dest_norm > 0:
                similarity = dot_product / (query_norm * dest_norm)
            else:
                similarity = 0
                
            scores.append((dest_id, similarity))
            
        # Sort by similarity desc
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Filter and Format Results
        results = []
        for dest_id, score in scores[:top_k]:
            if score > 0.05: # Minimum relevance threshold
                dest = self.destinations[dest_id]
                results.append({
                    'id': dest_id,
                    'name': dest['name'],
                    'match_score': round(score * 100, 1),
                    'type': dest['type'],
                    'eco_score': dest['eco_score'],
                    'description': dest['description']
                })
                
        return results

    def get_suggestions(self, context_type):
        """Get suggestions based on a type category (simple filter fallback)"""
        results = []
        for dest_id, data in self.destinations.items():
            if context_type in data.get('type', []):
                results.append({
                    'id': dest_id,
                    'name': data['name'],
                    'match_score': 90, # High confidence for direct type match
                    'type': data['type'],
                    'eco_score': data['eco_score'],
                    'description': data['description']
                })
        return results[:3]
