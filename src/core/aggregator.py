class ResultAggregator:
    """
    Combines results from multiple modules into a single response.
    """

    def combine(self, results):
        """
        Combine module results into a single string.

        Args:
            results (list[str]): List of results from executed tasks

        Returns:
            str: Final combined response
        """

        if not results:
            return "No results were produced."

        # Remove empty or None results
        cleaned_results = [str(r).strip() for r in results if r]

        if not cleaned_results:
            return "Tasks executed but no useful results were returned."

        # Join results with spacing for readability
        combined_response = "\n\n".join(cleaned_results)

        return combined_response