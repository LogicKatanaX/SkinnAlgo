"""
Cosmeceutical Chemical Knowledge Graph.
Comprehensive database of 28 verified dermatological and cosmeceutical active compounds,
their biochemical Mechanisms of Action (MOA), pH stability, and contraindications.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CosmeceuticalCompound:
    """Detailed chemical and clinical profile for a cosmeceutical active compound."""
    id: str
    name: str
    inci_name: str
    chemical_class: str               # "BHA", "AHA", "Retinoid", "Barrier Lipid", "Tyrosinase Inhibitor", etc.
    typical_concentration: str        # e.g., "2%"
    optimal_ph: str                   # e.g., "3.0 - 4.0"
    target_concerns: List[str]        # ["acne", "sebum", "texture", "hyperpigmentation", "erythema", "barrier"]
    mechanism_of_action: str          # Biochemical MOA
    photosensitizing: bool            # Requires mandatory SPF 50+
    recommended_timing: str           # "AM", "PM", "AM/PM", "PM_ONLY"
    search_query_template: str        # Exact copy-paste e-commerce search query
    contraindicated_with: List[str] = field(default_factory=list)


# 28 Verified Clinical Cosmeceutical Actives
COMPOUND_DATABASE: Dict[str, CosmeceuticalCompound] = {
    "salicylic_acid": CosmeceuticalCompound(
        id="salicylic_acid",
        name="Salicylic Acid",
        inci_name="Salicylic Acid",
        chemical_class="BHA (Beta Hydroxy Acid)",
        typical_concentration="2.0%",
        optimal_ph="3.0 - 3.8",
        target_concerns=["acne", "sebum", "texture", "comedones"],
        mechanism_of_action="Lipophilic desmolytic keratolytic that penetrates deep into the sebaceous follicle, dissolving the lipid desmosomes cementing dead keratinocytes and preventing microcomedone formation.",
        photosensitizing=False,
        recommended_timing="PM",
        search_query_template="2% Salicylic Acid BHA Liquid Exfoliant fragrance-free",
        contraindicated_with=["adapalene", "retinol", "retinaldehyde", "glycolic_acid"]
    ),
    "adapalene": CosmeceuticalCompound(
        id="adapalene",
        name="Micronized Adapalene",
        inci_name="Adapalene",
        chemical_class="Retinoid (3rd Generation)",
        typical_concentration="0.1%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["acne", "texture", "comedones"],
        mechanism_of_action="Selective RAR-beta and RAR-gamma receptor agonist that normalizes follicular epithelial cell differentiation, reduces keratinization, and exhibits potent indirect anti-inflammatory activity by suppressing leukotriene synthesis.",
        photosensitizing=True,
        recommended_timing="PM_ONLY",
        search_query_template="0.1% Adapalene Gel acne treatment unscented",
        contraindicated_with=["salicylic_acid", "glycolic_acid", "lactic_acid", "benzoyl_peroxide"]
    ),
    "retinol": CosmeceuticalCompound(
        id="retinol",
        name="Stabilized Retinol",
        inci_name="Retinol",
        chemical_class="Retinoid (1st Generation)",
        typical_concentration="0.2% - 0.5%",
        optimal_ph="5.5 - 6.5",
        target_concerns=["texture", "hyperpigmentation", "cellular_turnover"],
        mechanism_of_action="Lipophilic alcohol form of Vitamin A that converts through retinaldehyde into retinoic acid, accelerating basal keratinocyte turnover and stimulating procollagen-I gene transcription in dermal fibroblasts.",
        photosensitizing=True,
        recommended_timing="PM_ONLY",
        search_query_template="0.3% Pure Retinol Serum encapsulated night treatment",
        contraindicated_with=["salicylic_acid", "glycolic_acid", "lactic_acid", "l_ascorbic_acid"]
    ),
    "retinaldehyde": CosmeceuticalCompound(
        id="retinaldehyde",
        name="Retinaldehyde (Retinal)",
        inci_name="Retinal",
        chemical_class="Retinoid (Direct Precursor)",
        typical_concentration="0.05% - 0.1%",
        optimal_ph="5.5 - 6.5",
        target_concerns=["acne", "texture", "hyperpigmentation"],
        mechanism_of_action="Direct one-step biochemical precursor to retinoic acid offering 11x faster conversion than retinol, with innate direct antibacterial action against Cutibacterium acnes via bacterial cell wall lysis.",
        photosensitizing=True,
        recommended_timing="PM_ONLY",
        search_query_template="0.05% Retinaldehyde Emulsion retinal night serum",
        contraindicated_with=["salicylic_acid", "glycolic_acid", "lactic_acid", "benzoyl_peroxide"]
    ),
    "benzoyl_peroxide": CosmeceuticalCompound(
        id="benzoyl_peroxide",
        name="Micronized Benzoyl Peroxide",
        inci_name="Benzoyl Peroxide",
        chemical_class="Oxidizing Antimicrobial",
        typical_concentration="2.5% - 5.0%",
        optimal_ph="4.5 - 6.0",
        target_concerns=["acne", "inflammatory_papules"],
        mechanism_of_action="Releases reactive oxygen species (ROS) inside the anaerobic pilosebaceous unit, destroying Cutibacterium acnes without inducing microbial antibiotic resistance.",
        photosensitizing=True,
        recommended_timing="AM",
        search_query_template="2.5% Micronized Benzoyl Peroxide water-based gel wash",
        contraindicated_with=["l_ascorbic_acid", "adapalene", "retinol", "retinaldehyde"]
    ),
    "azelaic_acid": CosmeceuticalCompound(
        id="azelaic_acid",
        name="Azelaic Acid",
        inci_name="Azelaic Acid",
        chemical_class="Dicarboxylic Acid",
        typical_concentration="10.0% - 15.0%",
        optimal_ph="4.0 - 5.0",
        target_concerns=["erythema", "acne", "hyperpigmentation", "rosacea"],
        mechanism_of_action="Competitively inhibits tyrosinase in hyperactive melanocytes, suppresses kallikrein-5 and cathelicidin expression in vascular erythema/rosacea, and normalizes keratinocyte maturation.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="10% Azelaic Acid Suspension soothing brightening treatment",
        contraindicated_with=[]
    ),
    "niacinamide": CosmeceuticalCompound(
        id="niacinamide",
        name="Niacinamide (Vitamin B3)",
        inci_name="Niacinamide",
        chemical_class="Sebum Regulator & Coenzyme Precursor",
        typical_concentration="3.0% - 5.0%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["sebum", "barrier", "erythema", "texture"],
        mechanism_of_action="Precursor to NAD+/NADH cellular energy currency; downregulates sebaceous squalene/triglyceride lipogenesis, stimulates sphingolipid and ceramide synthesis, and inhibits melanosome transfer to keratinocytes.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="5% Niacinamide Serum with Zinc PCA barrier support",
        contraindicated_with=[]
    ),
    "zinc_pca": CosmeceuticalCompound(
        id="zinc_pca",
        name="Zinc PCA",
        inci_name="Zinc PCA",
        chemical_class="Sebum Modulator & NMF",
        typical_concentration="1.0%",
        optimal_ph="5.0 - 6.0",
        target_concerns=["sebum", "acne", "bacterial_flora"],
        mechanism_of_action="Competitively inhibits 5-alpha reductase enzyme to suppress DHT-mediated sebum hypersecretion while pyrrolidone carboxylic acid binds water to preserve stratum corneum hydration.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Zinc PCA 1% Niacinamide oil-control serum",
        contraindicated_with=[]
    ),
    "ceramides_np_ap_eop": CosmeceuticalCompound(
        id="ceramides_np_ap_eop",
        name="Physiological Ceramides (NP, AP, EOP)",
        inci_name="Ceramide NP, Ceramide AP, Ceramide EOP",
        chemical_class="Stratum Corneum Barrier Lipid",
        typical_concentration="3:1:1 Ratio (Ceramides : Cholesterol : Free Fatty Acids)",
        optimal_ph="5.0 - 5.8",
        target_concerns=["barrier", "erythema", "dehydration"],
        mechanism_of_action="Reconstructs the multi-lamellar lipid bilayers of the stratum corneum, restoring epidermal cohesion, preventing transepidermal water loss (TEWL), and insulating nociceptive nerve endings from irritants.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Physiological Ceramide 3:1:1 Barrier Repair Cream fragrance-free",
        contraindicated_with=[]
    ),
    "tranexamic_acid": CosmeceuticalCompound(
        id="tranexamic_acid",
        name="Tranexamic Acid",
        inci_name="Tranexamic Acid",
        chemical_class="Synthetic Lysine Derivative / Plasmin Inhibitor",
        typical_concentration="3.0% - 5.0%",
        optimal_ph="5.5 - 6.5",
        target_concerns=["hyperpigmentation", "melasma", "erythema"],
        mechanism_of_action="Reversibly blocks lysine binding sites on plasminogen molecules, suppressing UV-induced plasmin activation and downstream arachidonic acid / prostaglandin release, dampening melanocyte hyperactivity.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="3% Tranexamic Acid Serum dark spot discolorations",
        contraindicated_with=[]
    ),
    "alpha_arbutin": CosmeceuticalCompound(
        id="alpha_arbutin",
        name="Alpha Arbutin",
        inci_name="Alpha-Arbutin",
        chemical_class="Hydroquinone Glycoside / Tyrosinase Inhibitor",
        typical_concentration="2.0%",
        optimal_ph="4.5 - 5.5",
        target_concerns=["hyperpigmentation", "melasma", "post_inflammatory_marks"],
        mechanism_of_action="Hydrolyzes to release trace bioavailable hydroquinone within melanocytes, selectively inhibiting melanosomal tyrosinase activity and blocking L-DOPA oxidation with minimal cytotoxicity.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="2% Alpha Arbutin Serum with Hyaluronic Acid brightening",
        contraindicated_with=[]
    ),
    "l_ascorbic_acid": CosmeceuticalCompound(
        id="l_ascorbic_acid",
        name="L-Ascorbic Acid (Pure Vitamin C)",
        inci_name="Ascorbic Acid",
        chemical_class="Direct Antioxidant",
        typical_concentration="10.0% - 15.0%",
        optimal_ph="2.8 - 3.5",
        target_concerns=["hyperpigmentation", "antioxidant_defense", "cellular_turnover"],
        mechanism_of_action="Direct electron donor that neutralizes reactive singlet oxygen and superoxide free radicals, donates cofactors for prolyl and lysyl hydroxylase in procollagen synthesis, and reduces dopaquinone.",
        photosensitizing=False,
        recommended_timing="AM",
        search_query_template="15% Pure Vitamin C L-Ascorbic Acid Ferulic Acid serum",
        contraindicated_with=["benzoyl_peroxide", "retinol", "retinaldehyde", "salicylic_acid"]
    ),
    "ethyl_ascorbic_acid": CosmeceuticalCompound(
        id="ethyl_ascorbic_acid",
        name="3-O-Ethyl Ascorbic Acid",
        inci_name="3-O-Ethyl Ascorbic Acid",
        chemical_class="Stabilized Etherified Vitamin C",
        typical_concentration="10.0%",
        optimal_ph="4.0 - 5.5",
        target_concerns=["hyperpigmentation", "antioxidant_defense"],
        mechanism_of_action="Stable lipophilic/hydrophilic etherified derivative that metabolizes into pure ascorbic acid within epidermal layers, inhibiting tyrosinase and free radical cascades without low pH irritation.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="10% Ethyl Ascorbic Acid Stable Vitamin C serum",
        contraindicated_with=[]
    ),
    "sodium_ascorbyl_phosphate": CosmeceuticalCompound(
        id="sodium_ascorbyl_phosphate",
        name="Sodium Ascorbyl Phosphate (SAP)",
        inci_name="Sodium Ascorbyl Phosphate",
        chemical_class="Stable Hydrophilic Vitamin C / Anti-Acne",
        typical_concentration="5.0%",
        optimal_ph="6.0 - 7.0",
        target_concerns=["acne", "sebum", "hyperpigmentation"],
        mechanism_of_action="Water-soluble salt of L-ascorbic acid that enzymatically cleaves into ascorbic acid in vivo, specifically preventing squalene lipid peroxidation and reducing C. acnes colonization.",
        photosensitizing=False,
        recommended_timing="AM",
        search_query_template="5% Sodium Ascorbyl Phosphate SAP Vitamin C anti-blemish serum",
        contraindicated_with=[]
    ),
    "glycolic_acid": CosmeceuticalCompound(
        id="glycolic_acid",
        name="Glycolic Acid",
        inci_name="Glycolic Acid",
        chemical_class="AHA (Alpha Hydroxy Acid)",
        typical_concentration="5.0% - 7.0%",
        optimal_ph="3.2 - 3.8",
        target_concerns=["texture", "hyperpigmentation", "cellular_turnover"],
        mechanism_of_action="Smallest molecular weight AHA that penetrates between corneocytes, chelating calcium ions from desmosomal junctions and inducing rapid stratum corneum desquamation.",
        photosensitizing=True,
        recommended_timing="PM_ONLY",
        search_query_template="7% Glycolic Acid Exfoliating Toning Solution",
        contraindicated_with=["adapalene", "retinol", "retinaldehyde", "salicylic_acid"]
    ),
    "lactic_acid": CosmeceuticalCompound(
        id="lactic_acid",
        name="Lactic Acid",
        inci_name="Lactic Acid",
        chemical_class="AHA & Natural Moisturizing Factor",
        typical_concentration="5.0% - 10.0%",
        optimal_ph="3.6 - 4.0",
        target_concerns=["texture", "dehydration", "hyperpigmentation"],
        mechanism_of_action="Chiral alpha hydroxy acid that induces controlled chemical exfoliation while its carboxylate anion acts as an endogenous humectant, increasing water-binding capacity in the stratum corneum.",
        photosensitizing=True,
        recommended_timing="PM_ONLY",
        search_query_template="5% Lactic Acid HA gentle superficial exfoliating serum",
        contraindicated_with=["adapalene", "retinol", "retinaldehyde"]
    ),
    "mandelic_acid": CosmeceuticalCompound(
        id="mandelic_acid",
        name="Mandelic Acid",
        inci_name="Mandelic Acid",
        chemical_class="Aromatic Lipophilic AHA",
        typical_concentration="10.0%",
        optimal_ph="3.5 - 4.2",
        target_concerns=["acne", "hyperpigmentation", "texture"],
        mechanism_of_action="Large molecular weight aromatic AHA derived from bitter almonds that penetrates slowly and uniformly, combining gentle desquamation with innate antibacterial action, ideal for sensitive skin.",
        photosensitizing=True,
        recommended_timing="PM_ONLY",
        search_query_template="10% Mandelic Acid gentle chemical peel serum",
        contraindicated_with=["adapalene", "retinol"]
    ),
    "gluconolactone": CosmeceuticalCompound(
        id="gluconolactone",
        name="Gluconolactone (PHA)",
        inci_name="Gluconolactone",
        chemical_class="PHA (Polyhydroxy Acid)",
        typical_concentration="4.0% - 8.0%",
        optimal_ph="3.8 - 4.5",
        target_concerns=["texture", "barrier", "erythema", "dehydration"],
        mechanism_of_action="Multiple hydroxyl group chelator that gently loosens corneocytes without penetrating into deep living epidermis, strengthening barrier cohesion and shielding against oxidative metal ions.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="4% PHA Gluconolactone Gentle Exfoliating toner sensitive skin",
        contraindicated_with=[]
    ),
    "centella_asiatica": CosmeceuticalCompound(
        id="centella_asiatica",
        name="Madecassoside / Centella Asiatica",
        inci_name="Madecassoside, Centella Asiatica Extract",
        chemical_class="Triterpenoid Anti-Inflammatory",
        typical_concentration="1.0% - 3.0%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["erythema", "barrier", "post_inflammatory_marks"],
        mechanism_of_action="Pentacyclic triterpene saponins downregulate pro-inflammatory cytokines (IL-1beta, TNF-alpha) and stimulate Type I and III collagen biosynthesis in basal dermis.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Madecassoside Centella Asiatica Cica barrier repair balm",
        contraindicated_with=[]
    ),
    "hyaluronic_acid_multi": CosmeceuticalCompound(
        id="hyaluronic_acid_multi",
        name="Multi-Weight Hyaluronic Acid",
        inci_name="Sodium Hyaluronate, Hydrolyzed Hyaluronic Acid",
        chemical_class="Multi-Molecular Humectant",
        typical_concentration="1.0% - 2.0%",
        optimal_ph="5.0 - 7.0",
        target_concerns=["dehydration", "barrier"],
        mechanism_of_action="High molecular weight HA forms an invisible moisture-binding matrix at the skin surface, while low molecular weight oligomers penetrate to bind up to 1000x their weight in water in deeper strata.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Multi-Molecular Hyaluronic Acid Serum hydrating booster",
        contraindicated_with=[]
    ),
    "panthenol": CosmeceuticalCompound(
        id="panthenol",
        name="Panthenol (Pro-Vitamin B5)",
        inci_name="Panthenol",
        chemical_class="Pro-Vitamin B5 / Epithelializer",
        typical_concentration="5.0%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["barrier", "erythema", "dehydration"],
        mechanism_of_action="Enzymatically oxidizes to pantothenic acid (coenzyme A constituent), accelerating stratum corneum lipid crystallization, fibroblast proliferation, and reducing transepidermal water loss.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="5% Panthenol B5 Soothing Barrier Repair Cream",
        contraindicated_with=[]
    ),
    "ectoin": CosmeceuticalCompound(
        id="ectoin",
        name="Ectoin",
        inci_name="Ectoin",
        chemical_class="Extremolyte Osmoprotectant",
        typical_concentration="1.0% - 2.0%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["barrier", "erythema", "environmental_stress"],
        mechanism_of_action="Surrounds biomacromolecules with dense hydratized water clusters ('Ectoin Hydro Complex'), stabilizing cell membranes, reducing UVA-induced AP-2 expression, and shielding against urban micro-particulates.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="2% Ectoin Anti-Stress Barrier Defense Serum",
        contraindicated_with=[]
    ),
    "allantoin": CosmeceuticalCompound(
        id="allantoin",
        name="Allantoin",
        inci_name="Allantoin",
        chemical_class="Keratoplastic & Soothing Agent",
        typical_concentration="0.5%",
        optimal_ph="4.5 - 6.0",
        target_concerns=["barrier", "erythema"],
        mechanism_of_action="Promotes natural desquamation of the stratum corneum through keratin hydration and encourages physiological tissue renewal without chemical irritation.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Allantoin Soothing Calming Gel Cream fragrance-free",
        contraindicated_with=[]
    ),
    "bakuchiol": CosmeceuticalCompound(
        id="bakuchiol",
        name="Bakuchiol",
        inci_name="Bakuchiol",
        chemical_class="Meroterpene Phenol (Phyto-Retinol Alternative)",
        typical_concentration="1.0%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["texture", "hyperpigmentation", "cellular_turnover"],
        mechanism_of_action="Upregulates retinoic acid receptor gene expression profiles without activating retinoic acid receptors directly, delivering retinol-like collagen upregulation without erythema or barrier peeling.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="1% Bakuchiol Botanical Retinol Alternative facial oil",
        contraindicated_with=[]
    ),
    "copper_tripeptide_1": CosmeceuticalCompound(
        id="copper_tripeptide_1",
        name="Copper Tripeptide-1 (GHK-Cu)",
        inci_name="Copper Tripeptide-1",
        chemical_class="Signal & Carrier Peptide",
        typical_concentration="1.0%",
        optimal_ph="5.5 - 6.5",
        target_concerns=["texture", "barrier", "cellular_turnover"],
        mechanism_of_action="Carrier tripeptide (Gly-His-Lys) carrying copper(II) ions that activates metalloproteinase remodelling, upregulates collagen and elastin synthesis, and suppresses TGF-beta inflammatory cascades.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Copper Tripeptide-1 GHK-Cu Repair Peptide Serum",
        contraindicated_with=["l_ascorbic_acid", "glycolic_acid", "salicylic_acid"]
    ),
    "colloidal_oat": CosmeceuticalCompound(
        id="colloidal_oat",
        name="Colloidal Oatmeal & Beta-Glucan",
        inci_name="Avena Sativa (Oat) Kernel Flour",
        chemical_class="Anti-Pruritic Hydrocolloid",
        typical_concentration="1.0% - 2.0%",
        optimal_ph="5.0 - 6.5",
        target_concerns=["barrier", "erythema"],
        mechanism_of_action="Rich in avenanthramides that suppress NF-kappaB activation and reduce histamine release, forming an occlusive water-binding colloidal film over compromised skin.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="Colloidal Oat 2% Eczema Relief Soothing Cream",
        contraindicated_with=[]
    ),
    "sulfur": CosmeceuticalCompound(
        id="sulfur",
        name="Precipitated Sulfur",
        inci_name="Sulfur",
        chemical_class="Keratolytic Antimicrobial",
        typical_concentration="3.0%",
        optimal_ph="5.5 - 7.0",
        target_concerns=["acne", "sebum", "inflammatory_papules"],
        mechanism_of_action="Reacts with cysteine in keratinocytes to form hydrogen sulfide, exerting mild keratolytic and antiparasitic activity while suppressing sebaceous gland hyperfunction.",
        photosensitizing=False,
        recommended_timing="PM",
        search_query_template="3% Sulfur Acne Treatment Ointment Wash",
        contraindicated_with=["benzoyl_peroxide"]
    ),
    "squalane": CosmeceuticalCompound(
        id="squalane",
        name="Biomimetic 100% Plant Squalane",
        inci_name="Squalane",
        chemical_class="Biomimetic Saturated Emollient",
        typical_concentration="100%",
        optimal_ph="Neutral (Non-aqueous)",
        target_concerns=["barrier", "dehydration"],
        mechanism_of_action="Hydrogenated saturated analog of natural sebum squalene that replenishes the intercellular lipid mantle, preventing transepidermal water loss without comedogenic pore clogging.",
        photosensitizing=False,
        recommended_timing="AM/PM",
        search_query_template="100% Plant-Derived Squalane Oil non-comedogenic",
        contraindicated_with=[]
    ),
}


class CosmeceuticalKnowledgeGraph:
    """
    Search and query engine for the cosmeceutical knowledge base.
    """

    def __init__(self):
        self.compounds = COMPOUND_DATABASE

    def get(self, compound_id: str) -> Optional[CosmeceuticalCompound]:
        return self.compounds.get(compound_id)

    def search_by_concern(self, concern: str) -> List[CosmeceuticalCompound]:
        """Find all compounds with a mechanism of action targeting a specific concern."""
        concern_lower = concern.lower()
        return [
            c for c in self.compounds.values()
            if any(concern_lower in tc for tc in c.target_concerns)
        ]

    def all_compounds(self) -> List[CosmeceuticalCompound]:
        return list(self.compounds.values())

    def get_by_ids(self, compound_ids: List[str]) -> List[CosmeceuticalCompound]:
        return [self.compounds[cid] for cid in compound_ids if cid in self.compounds]

