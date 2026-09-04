-- Lactavia sample supply-chain data for Unity Catalog.
-- Run in the Databricks SQL editor against warehouse ec3c62eb69ad9330,
-- or via: python scripts/seed_databricks.py
--
-- Targets the existing `lactavia` catalog. The metastore uses Default Storage, so
-- catalogs must be created from the UI rather than with plain CREATE CATALOG.
--
-- Table and column comments are what Genie uses to pick tables and write SQL,
-- so keep them descriptive when you extend this file.

CREATE SCHEMA IF NOT EXISTS lactavia.supply_chain
  COMMENT 'Plants, products, suppliers and ingredient inventory for the Lactavia supply disruption demo.';

-- ---------------------------------------------------------------- plants

CREATE OR REPLACE TABLE lactavia.supply_chain.plants (
  plant_id            STRING  COMMENT 'Plant identifier, for example PLANT-FR-01.',
  plant_name          STRING  COMMENT 'Lactavia manufacturing site name.',
  city                STRING  COMMENT 'City where the plant operates.',
  country             STRING  COMMENT 'Country where the plant operates.',
  region              STRING  COMMENT 'Two-letter market region served by the plant (FR, BE, DE, ES).',
  production_lines    INT     COMMENT 'Number of active production lines at the plant.',
  capacity_units_day  BIGINT  COMMENT 'Total finished-goods capacity in consumer units per day.',
  utilization_pct     DOUBLE  COMMENT 'Average line utilization as a percentage of capacity.'
) COMMENT 'Lactavia manufacturing sites and their finished-goods capacity.';

INSERT INTO lactavia.supply_chain.plants VALUES
  ('PLANT-FR-01', 'Lactavia Rennes',    'Rennes',    'France',  'FR', 3, 222000, 87.0),
  ('PLANT-BE-01', 'Lactavia Ghent',     'Ghent',     'Belgium', 'BE', 2, 138000, 84.0),
  ('PLANT-DE-02', 'Lactavia Bielefeld', 'Bielefeld', 'Germany', 'DE', 3, 196000, 79.0),
  ('PLANT-ES-01', 'Lactavia Girona',    'Girona',    'Spain',   'ES', 2, 104000, 71.0);

-- -------------------------------------------------------------- products

CREATE OR REPLACE TABLE lactavia.supply_chain.products (
  sku_id                STRING  COMMENT 'Finished-goods SKU identifier, for example SKU-YOG-001.',
  sku_name              STRING  COMMENT 'Commercial product name.',
  brand                 STRING  COMMENT 'Lactavia brand the SKU belongs to.',
  category              STRING  COMMENT 'Product category: yogurt, dessert or drink.',
  primary_plant_id      STRING  COMMENT 'Plant that produces most of the volume for this SKU, joins to plants.plant_id.',
  region                STRING  COMMENT 'Primary market region for the SKU.',
  units_per_week        BIGINT  COMMENT 'Average weekly sales volume in consumer units.',
  revenue_per_unit_eur  DOUBLE  COMMENT 'Net revenue per consumer unit in euros.',
  margin_pct            DOUBLE  COMMENT 'Gross margin as a percentage of net revenue.',
  strategic_tier        STRING  COMMENT 'Commercial importance: flagship, core or tail.',
  uses_pectin_450       BOOLEAN COMMENT 'TRUE when the recipe requires high-methoxyl pectin ING-PEC-450.'
) COMMENT 'Lactavia finished-goods SKUs with weekly volume and profitability.';

INSERT INTO lactavia.supply_chain.products VALUES
  ('SKU-YOG-001', 'Naturel Strawberry Yogurt 4x125g', 'Lactavia Naturel',   'yogurt',  'PLANT-FR-01', 'FR', 412000, 2.65, 31.5, 'flagship', TRUE),
  ('SKU-YOG-002', 'Naturel Peach Yogurt 4x125g',      'Lactavia Naturel',   'yogurt',  'PLANT-FR-01', 'FR', 186000, 2.65, 30.8, 'core',     TRUE),
  ('SKU-YOG-003', 'Naturel Cherry Yogurt 4x125g',     'Lactavia Naturel',   'yogurt',  'PLANT-BE-01', 'BE', 121000, 2.72, 29.4, 'core',     TRUE),
  ('SKU-YOG-004', 'Selection Layered Vanilla 150g',   'Lactavia Selection', 'dessert', 'PLANT-FR-01', 'FR',  94000, 3.40, 34.2, 'core',     TRUE),
  ('SKU-YOG-006', 'Kids Pouch Berry 4x90g',           'Lactavia Kids',      'yogurt',  'PLANT-FR-01', 'FR', 158000, 2.20, 27.6, 'core',     FALSE),
  ('SKU-YOG-011', 'Naturel Plain Yogurt 4x125g',      'Lactavia Naturel',   'yogurt',  'PLANT-DE-02', 'DE', 203000, 2.10, 26.9, 'core',     FALSE),
  ('SKU-DRK-020', 'Drink Mango 6x100ml',              'Lactavia Go',        'drink',   'PLANT-ES-01', 'ES',  87000, 1.95, 24.5, 'tail',     TRUE),
  ('SKU-DES-031', 'Selection Chocolate Pot 2x110g',   'Lactavia Selection', 'dessert', 'PLANT-DE-02', 'DE',  76000, 3.10, 33.0, 'tail',     FALSE);

-- ------------------------------------------------------------- suppliers

CREATE OR REPLACE TABLE lactavia.supply_chain.suppliers (
  supplier_id            STRING  COMMENT 'Supplier identifier, for example SUP-EU-014.',
  supplier_name          STRING  COMMENT 'Legal name of the supplier.',
  country                STRING  COMMENT 'Country the supplier ships from.',
  ingredient_id          STRING  COMMENT 'Ingredient supplied, for example ING-PEC-450 (high-methoxyl pectin).',
  qualification_status   STRING  COMMENT 'Qualification state: qualified, in_qualification or unqualified.',
  lead_time_days         INT     COMMENT 'Order-to-delivery lead time in days.',
  capacity_kg_per_month  BIGINT  COMMENT 'Monthly volume the supplier can commit, in kilograms.',
  unit_price_eur         DOUBLE  COMMENT 'Price per kilogram in euros.',
  reliability_score      DOUBLE  COMMENT 'On-time in-full reliability between 0 and 1.',
  contract_status        STRING  COMMENT 'Contract state: active, force_majeure_declared or spot_only.'
) COMMENT 'Ingredient suppliers for Lactavia, including the pectin sources affected by the 2026 disruption.';

INSERT INTO lactavia.supply_chain.suppliers VALUES
  ('SUP-EU-014', 'Valencia Pectinas S.A.',       'Spain',       'ING-PEC-450', 'qualified',        45, 220000, 14.20, 0.62, 'force_majeure_declared'),
  ('SUP-EU-023', 'Rheinland Hydrocolloids GmbH', 'Germany',     'ING-PEC-450', 'qualified',        21,  40000, 16.76, 0.94, 'active'),
  ('SUP-EU-031', 'Nordic Botanic Extracts AB',   'Sweden',      'ING-PEC-450', 'in_qualification', 35,  65000, 18.40, 0.88, 'spot_only'),
  ('SUP-LA-007', 'Andes Citrus Pectin Ltda.',    'Brazil',      'ING-PEC-450', 'unqualified',      60, 150000, 12.90, 0.71, 'spot_only'),
  ('SUP-EU-045', 'Benelux Dairy Cooperative',    'Netherlands', 'ING-MLK-001', 'qualified',         3, 900000,  0.48, 0.97, 'active'),
  ('SUP-EU-052', 'Loire Sucre S.A.',             'France',      'ING-SUG-100', 'qualified',        10, 400000,  0.86, 0.95, 'active');

-- --------------------------------------------------- ingredient_inventory

CREATE OR REPLACE TABLE lactavia.supply_chain.ingredient_inventory (
  inventory_id          STRING  COMMENT 'Inventory record identifier.',
  plant_id              STRING  COMMENT 'Plant holding the stock, joins to plants.plant_id.',
  ingredient_id         STRING  COMMENT 'Ingredient held in stock, for example ING-PEC-450.',
  ingredient_name       STRING  COMMENT 'Readable ingredient name.',
  quantity_kg           DOUBLE  COMMENT 'Quantity currently on hand in kilograms.',
  safety_stock_kg       DOUBLE  COMMENT 'Safety stock floor in kilograms.',
  daily_consumption_kg  DOUBLE  COMMENT 'Average daily consumption in kilograms.',
  days_of_cover         INT     COMMENT 'Days of production covered by the stock on hand.',
  stockout_date         DATE    COMMENT 'Forecast date the plant runs out of this ingredient.',
  last_replenished      DATE    COMMENT 'Date of the last goods receipt.'
) COMMENT 'Ingredient stock on hand per Lactavia plant with forecast stockout dates.';

INSERT INTO lactavia.supply_chain.ingredient_inventory VALUES
  ('INV-FR01-PEC450', 'PLANT-FR-01', 'ING-PEC-450', 'High-methoxyl pectin',   3720,  6200,   310, 12, DATE'2026-09-15', DATE'2026-08-14'),
  ('INV-DE02-PEC450', 'PLANT-DE-02', 'ING-PEC-450', 'High-methoxyl pectin',   3600,  4800,   240, 15, DATE'2026-09-18', DATE'2026-08-19'),
  ('INV-BE01-PEC450', 'PLANT-BE-01', 'ING-PEC-450', 'High-methoxyl pectin',   3330,  3700,   185, 18, DATE'2026-09-21', DATE'2026-08-21'),
  ('INV-ES01-PEC450', 'PLANT-ES-01', 'ING-PEC-450', 'High-methoxyl pectin',   2100,  2400,   120, 17, DATE'2026-09-20', DATE'2026-08-23'),
  ('INV-FR01-MLK001', 'PLANT-FR-01', 'ING-MLK-001', 'Raw milk',             148000, 90000, 21000,  7, DATE'2026-09-10', DATE'2026-09-01'),
  ('INV-DE02-SUG100', 'PLANT-DE-02', 'ING-SUG-100', 'Cane sugar',            62000, 30000,  4100, 15, DATE'2026-09-18', DATE'2026-08-28');
