import re
import statistics

# using set values for buckets in the timeline
GEOLOGICAL_TIMELINE_REGISTRY = {
    # --- QUATERNARY PERIOD ---
    "Holocene": (r'\b(Holocene|Recent\s*Epoch|Post\s*Glacial)\b', 11700, 0),
    "Younger Dryas": (r'\b(Younger\s*Dryas|Big\s*Freeze)\b', 12900, 11700),
    "Pleistocene": (r'\b(Pleistocene|Ice\s*Age|Glacial\s*Maximum|LGM|Great\s*Ice\s*Age)\b', 2580000, 11700),

    # --- NEOGENE PERIOD ---
    "Pliocene": (r'\b(Pliocene)\b', 5333000, 2580000),
    "Miocene": (r'\b(Miocene)\b', 23030000, 5333000),

    # --- PALEOGENE PERIOD ---
    "Oligocene": (r'\b(Oligocene)\b', 33900000, 23030000),
    "Eocene": (r'\b(Eocene)\b', 56000000, 33900000),
    "Paleocene": (r'\b(Paleocene)\b', 66000000, 56000000),

    # --- BROAD OVERARCHING ERAS ---
    "Cenozoic": (r'\b(Cenozoic|Age\s*of\s*Mammals)\b', 66000000, 0),
    "Mesozoic": (r'\b(Mesozoic|Age\s*of\s*Dinosaurs|Cretaceous|Jurassic|Triassic)\b', 252000000, 66000000)
}

# Setting start/end dates for the timeline
GEOLOGICAL_ROSETTA_STONE = [
    {"epoch": "Holocene", "start": 0, "end": 11700},
    {"epoch": "Pleistocene", "start": 11701, "end": 2580000},
    {"epoch": "Pliocene", "start": 2580001, "end": 5333000},
    {"epoch": "Miocene", "start": 5333001, "end": 23030000},
    {"epoch": "Oligocene", "start": 23030001, "end": 33900000},
    {"epoch": "Eocene", "start": 33900001, "end": 56000000},
    {"epoch": "Paleocene", "start": 56000001, "end": 66000000},
    {"epoch": "Cretaceous", "start": 66000001, "end": 145000000},
    {"epoch": "Jurassic", "start": 145000001, "end": 201300000},
    {"epoch": "Triassic", "start": 201300001, "end": 251902000}
]


class Language_Processing:
    def __init__(self,transcript):
        self.transcript = transcript


    #a test method to see how NLP was working
    def extract_geological_context(self):
        context_summary = {}

        print("--- Executing Thorough Geological Scan ---")
        for epoch_name, (pattern, start_yr, end_yr) in GEOLOGICAL_TIMELINE_REGISTRY.items():
            matches = re.findall(pattern, self.transcript, re.IGNORECASE)
            match_count = len(matches)

            if match_count > 0:
                context_summary[epoch_name] = {
                    "mentions": match_count,
                    "raw_matches": list(set([m.strip().title() for m in matches])),
                    "timespan": f"{start_yr:,} to {end_yr:,} years ago"
                }

        return context_summary


    # standardizing dates used in following methods
    def standardize_prehistoric_dates(self):
        """
        Scans the text for chronological variations and standardizes
        them into absolute integer formats (Years Before Present).
        """
        found_dates = []

        #finding millions
        million_pattern = r'(\d[\d,.]*)\s*million\s*years?\s*ago'
        for match in re.finditer(million_pattern, self.transcript, re.IGNORECASE):
            num_val = float(match.group(1).replace(',', ''))
            standardized_integer = int(num_val * 1_000_000)
            found_dates.append(standardized_integer)

        #finding thousands
        range_pattern = r'\b(\d[\d,.]*)\s*and\s*(\d[\d,.]*)\s*000\s*years?\s*ago|\b(\d[\d,.]*)\s*and\s*(\d[\d,.]*),000\s*years?\s*ago'

        #more explicit thousands
        thousand_pattern = r'(\d[\d,.]*)\s*years?\s*ago'

        for match in re.finditer(thousand_pattern, self.transcript, re.IGNORECASE):
            raw_num = match.group(1).replace(',', '')

            #filtering out things already caught in million year filter
            if "million" in self.transcript[max(0, match.start() - 10):match.end()]:
                continue
            try:
                num_val = float(raw_num)
                if num_val < 1000 and num_val > 0:
                    num_val = num_val * 1000
                found_dates.append(int(num_val))
            except ValueError:
                pass

        return sorted(list(set(found_dates)))


    # extracting actual standardized integers and geological keywords
    def extract_features(self):

        extracted_integers = self.standardize_prehistoric_dates()
        keyword_counts = {}
        for epoch_name, (pattern, _, _) in GEOLOGICAL_TIMELINE_REGISTRY.items():
            matches = re.findall(pattern, self.transcript, re.IGNORECASE)
            if matches:
                keyword_counts[epoch_name] = len(matches)

        return extracted_integers, keyword_counts


    #Calculates useable anchor, most likely epoch, and the certainty by the number of references
    def calculate_anchor_point(self,extracted_integers, keyword_counts):

        if not extracted_integers:
            return 0, "Unknown Era", "LOW"

        era_votes = {period["epoch"]: 0 for period in GEOLOGICAL_ROSETTA_STONE}
        era_votes["Younger Dryas"] = 0

        for epoch, count in keyword_counts.items():
            if epoch in era_votes:
                era_votes[epoch] += count

        for date in extracted_integers:
            for period in GEOLOGICAL_ROSETTA_STONE:
                if period["start"] <= date <= period["end"]:
                    era_votes[period["epoch"]] += 1
                    break

        primary_epoch = max(era_votes, key=era_votes.get)
        total_votes = sum(era_votes.values())
        winning_votes = era_votes[primary_epoch]

        confidence_pct = (winning_votes / total_votes) * 100 if total_votes > 0 else 0

        boundary = next((p for p in GEOLOGICAL_ROSETTA_STONE if p["epoch"] == primary_epoch), None)

        valid_dates = []
        if boundary:
            for date in extracted_integers:
                buffer = boundary["end"] * 0.20
                if (boundary["start"] - buffer) <= date <= (boundary["end"] + buffer):
                    valid_dates.append(date)
                elif primary_epoch == "Pleistocene" and date == 11000:
                    valid_dates.append(date)

        if not valid_dates:
            valid_dates = extracted_integers

        final_anchor = int(statistics.median(valid_dates))

        confidence_label = f"{confidence_pct:.1f}% consensus for {primary_epoch}"

        return final_anchor, primary_epoch, confidence_label

