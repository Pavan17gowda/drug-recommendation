/**
 * Recommendations Service
 * Handles recommendation logic and drug database
 */

class RecommendationsService {
    constructor(apiService, storeService) {
        this.api = apiService;
        this.store = storeService;
        this.drugDatabase = this.initDrugDatabase();
        this.diseaseMapping = this.initDiseaseMapping();
    }

    /**
     * Initialize drug recommendations database
     */
    initDrugDatabase() {
        return {
            // Common Symptoms
            fever: ['Acetaminophen (Tylenol)', 'Ibuprofen (Advil)'],
            headache: ['Acetaminophen (Tylenol)', 'Ibuprofen (Advil)', 'Aspirin'],
            muscle_aches: ['Ibuprofen (Advil)', 'Naproxen (Aleve)'],
            joint_pain: ['Ibuprofen (Advil)', 'Naproxen (Aleve)'],
            
            // Respiratory Symptoms
            runny_nose: ['Loratadine (Claritin)', 'Cetirizine (Zyrtec)'],
            sneezing: ['Loratadine (Claritin)', 'Cetirizine (Zyrtec)', 'Fexofenadine (Allegra)'],
            shortness_of_breath: ['Albuterol Inhaler'],
            wheezing: ['Albuterol Inhaler', 'Fluticasone (Flovent)'],
            asthma: ['Albuterol Inhaler', 'Fluticasone (Flovent)'],
            sinus_infection: ['Amoxicillin', 'Azithromycin'],
            
            // Digestive Symptoms
            heartburn: ['Omeprazole (Prilosec)', 'Famotidine (Pepcid)'],
            acid_reflux: ['Omeprazole (Prilosec)', 'Esomeprazole (Nexium)'],
            stomach_pain: ['Bismuth subsalicylate (Pepto-Bismol)', 'Simethicone (Gas-X)'],
            
            // Chronic Conditions
            high_blood_pressure: ['Lisinopril', 'Amlodipine'],
            type_2_diabetes: ['Metformin', 'Glipizide'],
            hypothyroidism: ['Levothyroxine'],
            
            // Mental Health
            depression: ['Sertraline (Zoloft)', 'Fluoxetine (Prozac)'],
            anxiety: ['Sertraline (Zoloft)', 'Escitalopram (Lexapro)'],
            
            // Other Symptoms
            itchy_eyes: ['Ketotifen eye drops', 'Artificial tears'],
            bacterial_infection: ['Amoxicillin', 'Azithromycin'],
            sore_throat: ['Acetaminophen (Tylenol)', 'Throat lozenges'],
            
            // Additional Symptoms
            fatigue: ['Vitamin B Complex', 'Iron Supplements'],
            dizziness: ['Meclizine (Antivert)', 'Dimenhydrinate (Dramamine)'],
            nausea: ['Ondansetron (Zofran)', 'Promethazine (Phenergan)'],
            vomiting: ['Prochlorperazine (Compazine)', 'Metoclopramide (Reglan)'],
            blurred_vision: ['Artificial Tears', 'Timolol (for glaucoma)'],
            chest_pain: ['Nitroglycerin (for angina)', 'Aspirin'],
            palpitations: ['Beta-blockers (Metoprolol)', 'Calcium channel blockers (Verapamil)'],
            sweating: ['Antiperspirants', 'Clonidine (for hyperhidrosis)'],
            dry_mouth: ['Biotene Oral Balance Gel', 'Saliva substitutes'],
            difficulty_swallowing: ['Throat lozenges', 'Thickening agents'],
            insomnia: ['Melatonin', 'Diphenhydramine (Benadryl)'],
            hair_loss: ['Minoxidil (Rogaine)', 'Finasteride (Propecia)'],
            skin_rash: ['Hydrocortisone cream', 'Antihistamines'],
            constipation: ['Polyethylene glycol (MiraLAX)', 'Docusate (Colace)'],
            diarrhea: ['Loperamide (Imodium)', 'Bismuth subsalicylate (Pepto-Bismol)'],
            loss_of_appetite: ['Megestrol acetate (Megace)', 'Cyproheptadine (Periactin)'],
            weight_loss: ['Megestrol acetate (Megace)', 'Nutritional supplements'],
            frequent_urination: ['Tolterodine (Detrol)', 'Oxybutynin (Ditropan)'],
            back_pain: ['Ibuprofen (Advil)', 'Acetaminophen (Tylenol)'],
            cold_intolerance: ['Levothyroxine (if hypothyroid)', 'Wear warmer clothing'],
            weight_gain: ['Diet and exercise', 'Consult healthcare provider']
        };
    }

    /**
     * Initialize disease mapping
     */
    initDiseaseMapping() {
        return {
            thyroid: ['fatigue', 'weight_gain', 'cold_intolerance'],
            heart_disease: ['shortness_of_breath', 'chest_pain', 'high_blood_pressure'],
            allergy: ['sneezing', 'itchy_eyes', 'runny_nose'],
            cold: ['sneezing', 'runny_nose', 'sore_throat'],
            dehydration: ['dry_mouth', 'dizziness', 'nausea'],
            anemia: ['fatigue', 'dizziness'],
            diabetes: ['frequent_urination', 'weight_loss', 'blurred_vision'],
            hypertension: ['headache', 'high_blood_pressure', 'dizziness'],
            insomnia_disorder: ['insomnia', 'anxiety'],
            asthma_disease: ['shortness_of_breath', 'wheezing']
        };
    }

    /**
     * Identify diseases based on symptoms
     */
    identifyDiseases(symptoms) {
        const identifiedDiseases = [];
        
        for (const [disease, diseaseSymptoms] of Object.entries(this.diseaseMapping)) {
            if (diseaseSymptoms.every(symptom => symptoms.includes(symptom))) {
                identifiedDiseases.push(disease.replace('_', ' '));
            }
        }
        
        return identifiedDiseases.length > 0 
            ? identifiedDiseases 
            : ['No specific disease identified'];
    }

    /**
     * Generate medication recommendations
     */
    generateRecommendations(symptoms, patientInfo) {
        const recommendations = new Set();
        
        // Get recommendations for each symptom
        symptoms.forEach(symptom => {
            if (this.drugDatabase[symptom]) {
                this.drugDatabase[symptom].forEach(drug => {
                    recommendations.add(drug);
                });
            }
        });
        
        // Convert to array
        let finalRecommendations = Array.from(recommendations);
        
        // Apply age-based filters
        if (parseInt(patientInfo.age) < 18) {
            finalRecommendations = finalRecommendations.filter(drug => 
                !drug.includes('Zoloft') && 
                !drug.includes('Prozac') && 
                !drug.includes('Lexapro')
            );
        }
        
        return finalRecommendations;
    }

    /**
     * Process symptoms and generate full recommendation
     */
    async processSymptoms(symptoms, patientInfo) {
        try {
            this.store.setLoading(true);
            this.store.clearError();

            // Identify diseases
            const diseases = this.identifyDiseases(symptoms);
            
            // Generate medication recommendations
            const medications = this.generateRecommendations(symptoms, patientInfo);

            // Create recommendation object
            const recommendation = {
                date: new Date().toISOString(),
                symptoms: symptoms,
                diseases: diseases,
                medications: medications,
                patientInfo: patientInfo
            };

            // Save to backend
            const response = await this.api.saveRecommendation(recommendation);

            if (response.success) {
                this.store.addRecommendation(response.recommendation);
                return {
                    success: true,
                    recommendation: response.recommendation
                };
            }

            throw new Error(response.message);
        } catch (error) {
            this.store.setError(error.message);
            return {
                success: false,
                message: error.message
            };
        } finally {
            this.store.setLoading(false);
        }
    }

    /**
     * Load all recommendations
     */
    async loadRecommendations() {
        try {
            this.store.setLoading(true);
            const response = await this.api.getRecommendations();

            if (response.success) {
                this.store.setRecommendations(response.history);
                return {
                    success: true,
                    recommendations: response.history
                };
            }

            throw new Error(response.message);
        } catch (error) {
            this.store.setError(error.message);
            return {
                success: false,
                message: error.message
            };
        } finally {
            this.store.setLoading(false);
        }
    }

    /**
     * Delete a recommendation
     */
    async deleteRecommendation(id) {
        try {
            this.store.setLoading(true);
            const response = await this.api.deleteRecommendation(id);

            if (response.success) {
                this.store.removeRecommendation(id);
                return { success: true };
            }

            throw new Error(response.message);
        } catch (error) {
            this.store.setError(error.message);
            return {
                success: false,
                message: error.message
            };
        } finally {
            this.store.setLoading(false);
        }
    }

    /**
     * Load statistics
     */
    async loadStatistics() {
        try {
            const response = await this.api.getStatistics();

            if (response.success) {
                this.store.setStatistics(response.statistics);
                return {
                    success: true,
                    statistics: response.statistics
                };
            }

            throw new Error(response.message);
        } catch (error) {
            console.error('Error loading statistics:', error);
            return {
                success: false,
                message: error.message
            };
        }
    }
}

// Create singleton instance
const recommendationsService = new RecommendationsService(api, store);

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = recommendationsService;
}
