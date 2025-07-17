/**
 * TypeScript types for the Activity Selector frontend.
 * These match the backend Pydantic models for type safety.
 */

export const PriceLevel = {
  FREE: "Free",
  LOW: "$",
  MEDIUM: "$$",
  HIGH: "$$$",
  LUXURY: "$$$$"
} as const;

export type PriceLevelType = typeof PriceLevel[keyof typeof PriceLevel];

export interface Activity {
  name: string;
  description?: string;
  price_level: PriceLevelType;
  location?: string;
  category: string;
  address?: string;
  phone?: string;
  past_orders?: string[];
  last_bill_price?: number;
  url?: string;
  notes?: string;
  last_visit_date?: string;
}

export interface Category {
  name: string;
  description?: string;
  sheet_name: string;
}

export interface ActivityRequest {
  category: string;
  price_level?: PriceLevelType;
  limit?: number;
}

export interface ActivityResponse {
  activities: Activity[];
  total_found: number;
  category: string;
  price_level?: PriceLevelType;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  loading: boolean;
} 