import { hotel } from "./hotel";
import { guestReviewHighlight, reviewSources } from "./hospitality";

/**
 * Dated, source-specific facts. Never combine platform scores or imply a live feed.
 * Research: research/apple-dominant-revision/conversion-evidence/findings.json.
 */
export const socialProofCheckedAt = "2026-10-20T06:55:42Z";
export const googleReviewSnapshot = {
  platform: "Google",
  score: 3.7,
  scale: 5,
  reviewCount: 1628,
  scoreLabel: "3.7 out of 5",
  countLabel: "1,628 Google reviews",
  checkedAt: socialProofCheckedAt,
  dateLabel: "Checked 20 October 2026",
  href: reviewSources[0].href,
  sourceUrl: "https://www.google.co.in/travel/hotels/entity/ChkI9IOdtNaKmJZrGg0vZy8xMWI2ZGc2bWszEAE",
  note: "A dated snapshot. See Google for the latest reviews.",
} as const;

export const guestReview = guestReviewHighlight;
export const guestReviewProfiles = reviewSources;

function walkingDirections(destination: string) {
  const params = new URLSearchParams({
    api: "1",
    origin: `${hotel.coordinates.latitude},${hotel.coordinates.longitude}`,
    destination,
    travelmode: "walking",
  });
  return `https://www.google.com/maps/dir/?${params.toString()}`;
}

export const proximityHighlights = [
  {
    id: "kashi-vishwanath",
    name: "Shri Kashi Vishwanath Temple",
    label: "Within walking distance",
    description: "Set out from Godowlia for the temple. Check current visitor and entry guidance before you go.",
    href: walkingDirections("Shri Kashi Vishwanath Temple, Lahori Tola, Varanasi"),
    action: "Walking directions",
    sourceUrl: "https://www.makemytrip.com/hotels/hotel_augusto-details-varanasi.html",
    checkedAt: socialProofCheckedAt,
  },
  {
    id: "dashashwamedh",
    name: "Dashashwamedh Ghat",
    label: "Within walking distance",
    description: "The riverfront is close enough to explore on foot. Let the lanes, weather and crowds set your pace.",
    href: walkingDirections("Dashashwamedh Ghat, Varanasi"),
    action: "Walking directions",
    sourceUrl: googleReviewSnapshot.sourceUrl,
    checkedAt: socialProofCheckedAt,
  },
  {
    id: "godowlia",
    name: "Godowlia",
    label: "Your neighbourhood",
    description: "Stay on August Kunda Road, opposite State Bank of India. Ask the hotel about your final vehicle drop-off.",
    href: hotel.mapsUrl,
    action: "Find the hotel",
    sourceUrl: googleReviewSnapshot.sourceUrl,
    checkedAt: socialProofCheckedAt,
  },
] as const;
