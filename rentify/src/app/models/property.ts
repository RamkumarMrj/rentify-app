export interface Property {
    id?: string;
    seller_id?: string;
    place: string;
    area: string;
    price: number;
    bedrooms: number;
    bathrooms: number;
    amenities: string[];
    description: string;
    image: string;
    likes?: number;
    interestedUsers?: string[];
}

