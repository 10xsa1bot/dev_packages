"""
Google PageSpeed Insights API Client

This module provides a client for interacting with the Google PageSpeed Insights API.
"""

import requests
from typing import Dict, Optional, List
from urllib.parse import quote


class PageSpeedClient:
    """Client for Google PageSpeed Insights API"""

    BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def __init__(self, api_key: str):
        """
        Initialize PageSpeed client

        Args:
            api_key: Google PageSpeed Insights API key
        """
        self.api_key = api_key

    def analyze_url(
        self,
        url: str,
        strategy: str = "mobile",
        categories: Optional[List[str]] = None
    ) -> Dict:
        """
        Analyze a URL using PageSpeed Insights API

        Args:
            url: URL to analyze
            strategy: 'mobile' or 'desktop'
            categories: List of categories to analyze
                       (performance, accessibility, best-practices, seo, pwa)

        Returns:
            Dict containing PageSpeed results
        """
        if categories is None:
            categories = ["performance", "accessibility", "best-practices", "seo"]

        params = {
            "url": url,
            "key": self.api_key,
            "strategy": strategy,
        }

        # Add categories
        for category in categories:
            params[f"category"] = category

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=60)
            response.raise_for_status()
            return self._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _parse_response(self, data: Dict) -> Dict:
        """
        Parse PageSpeed API response and extract relevant data

        Args:
            data: Raw API response

        Returns:
            Parsed response with scores and metrics
        """
        try:
            lighthouse_result = data.get("lighthouseResult", {})
            categories = lighthouse_result.get("categories", {})

            scores = {
                "performance": self._get_score(categories.get("performance")),
                "accessibility": self._get_score(categories.get("accessibility")),
                "best_practices": self._get_score(categories.get("best-practices")),
                "seo": self._get_score(categories.get("seo")),
            }

            # Get metrics
            audits = lighthouse_result.get("audits", {})
            metrics = {
                "first_contentful_paint": self._get_metric(audits.get("first-contentful-paint")),
                "largest_contentful_paint": self._get_metric(audits.get("largest-contentful-paint")),
                "total_blocking_time": self._get_metric(audits.get("total-blocking-time")),
                "cumulative_layout_shift": self._get_metric(audits.get("cumulative-layout-shift")),
                "speed_index": self._get_metric(audits.get("speed-index")),
            }

            return {
                "success": True,
                "url": data.get("id"),
                "scores": scores,
                "metrics": metrics,
                "fetch_time": data.get("analysisUTCTimestamp")
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to parse response: {str(e)}"
            }

    def _get_score(self, category: Optional[Dict]) -> Optional[float]:
        """Extract score from category (0-100)"""
        if not category:
            return None
        score = category.get("score")
        if score is not None:
            return round(score * 100, 1)
        return None

    def _get_metric(self, audit: Optional[Dict]) -> Optional[Dict]:
        """Extract metric value and display value"""
        if not audit:
            return None
        return {
            "value": audit.get("numericValue"),
            "display": audit.get("displayValue"),
            "score": audit.get("score")
        }
