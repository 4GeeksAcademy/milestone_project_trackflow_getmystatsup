import type { Carrier, Product, Shipment } from "../types/domain.js";
export declare function validateProduct(product: Product): {
    valid: boolean;
    errors: string[];
};
export declare function validateShipment(shipment: Shipment): {
    valid: boolean;
    errors: string[];
};
export declare function validateCarrier(carrier: Carrier): {
    valid: boolean;
    errors: string[];
};
