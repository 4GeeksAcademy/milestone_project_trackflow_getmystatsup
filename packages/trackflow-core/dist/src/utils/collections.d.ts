import type { Carrier, Product, ProductCategory, WarehouseLocation } from "../types/domain.js";
export declare function filterProductsByWarehouse(products: Product[], warehouse: WarehouseLocation): Product[];
export declare function filterProductsByCategory(products: Product[], category: ProductCategory): Product[];
export declare function filterLowStockProducts(products: Product[]): Product[];
export declare function sortProductsByStock(products: Product[], order: "asc" | "desc"): Product[];
export declare function sortCarriersByReliability(carriers: Carrier[], order: "asc" | "desc"): Carrier[];
