/**
 * Service de validation pour les formulaires
 * Fournit des méthodes de validation réutilisables pour tous les formulaires de l'application
 */

// Types pour les règles de validation
type ValidationRule = (value: any, options?: any) => boolean | string;
type ValidationOptions = Record<string, any>;

// Interface pour les résultats de validation
interface ValidationResult {
  valid: boolean;
  message?: string;
}

// Classe principale du service de validation
export class ValidationService {
  /**
   * Valide une valeur selon une ou plusieurs règles
   * @param value - Valeur à valider
   * @param rules - Tableau de règles de validation
   * @param options - Options supplémentaires pour la validation
   * @returns Résultat de validation
   */
  static validate(
    value: any, 
    rules: Array<{ rule: ValidationRule; message?: string; options?: ValidationOptions }>,
    fieldName: string = 'Ce champ'
  ): ValidationResult {
    for (const { rule, message, options } of rules) {
      const result = rule(value, options);
      
      if (result === false || typeof result === 'string') {
        return {
          valid: false,
          message: typeof result === 'string' ? result : message || `${fieldName} n'est pas valide.`
        };
      }
    }
    
    return { valid: true };
  }

  // Règles de validation communes

  /**
   * Vérifie si une valeur est requise (non vide)
   */
  static required(value: any): boolean {
    if (value === null || value === undefined) return false;
    if (typeof value === 'string') return value.trim().length > 0;
    if (Array.isArray(value)) return value.length > 0;
    return true;
  }

  /**
   * Vérifie si une valeur est une adresse email valide
   */
  static email(value: string): boolean {
    if (!value) return true; // Si vide, laissez required gérer cela
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(value);
  }

  /**
   * Vérifie si une valeur a une longueur minimale
   */
  static minLength(value: string, options: { min: number }): boolean | string {
    if (!value) return true; // Si vide, laissez required gérer cela
    return value.length >= options.min || 
      `Ce champ doit contenir au moins ${options.min} caractères.`;
  }

  /**
   * Vérifie si une valeur a une longueur maximale
   */
  static maxLength(value: string, options: { max: number }): boolean | string {
    if (!value) return true;
    return value.length <= options.max || 
      `Ce champ ne doit pas dépasser ${options.max} caractères.`;
  }

  /**
   * Vérifie si une valeur est un nombre
   */
  static isNumber(value: any): boolean {
    if (!value && value !== 0) return true;
    return !isNaN(Number(value));
  }

  /**
   * Vérifie si une valeur est un entier
   */
  static isInteger(value: any): boolean {
    if (!value && value !== 0) return true;
    return Number.isInteger(Number(value));
  }

  /**
   * Vérifie si une valeur est dans une plage numérique
   */
  static range(value: number, options: { min?: number; max?: number }): boolean | string {
    if (value === null || value === undefined) return true;
    
    const numValue = Number(value);
    if (isNaN(numValue)) return false;
    
    if (options.min !== undefined && options.max !== undefined) {
      return (numValue >= options.min && numValue <= options.max) || 
        `Ce champ doit être compris entre ${options.min} et ${options.max}.`;
    } else if (options.min !== undefined) {
      return numValue >= options.min || 
        `Ce champ doit être supérieur ou égal à ${options.min}.`;
    } else if (options.max !== undefined) {
      return numValue <= options.max || 
        `Ce champ doit être inférieur ou égal à ${options.max}.`;
    }
    
    return true;
  }

  /**
   * Vérifie si une valeur correspond à un motif regex
   */
  static pattern(value: string, options: { regex: RegExp; }): boolean {
    if (!value) return true;
    return options.regex.test(value);
  }

  /**
   * Vérifie si une valeur de date est valide
   */
  static isDate(value: string): boolean {
    if (!value) return true;
    const date = new Date(value);
    return !isNaN(date.getTime());
  }

  /**
   * Vérifie si une date est dans le futur
   */
  static isFutureDate(value: string): boolean | string {
    if (!value) return true;
    const date = new Date(value);
    if (isNaN(date.getTime())) return false;
    
    const now = new Date();
    return date > now || "La date doit être dans le futur.";
  }

  /**
   * Vérifie si une date est dans le passé
   */
  static isPastDate(value: string): boolean | string {
    if (!value) return true;
    const date = new Date(value);
    if (isNaN(date.getTime())) return false;
    
    const now = new Date();
    return date < now || "La date doit être dans le passé.";
  }

  /**
   * Vérifie si deux valeurs sont égales (utile pour la confirmation de mot de passe)
   */
  static matches(value: any, options: { field: any }): boolean | string {
    return value === options.field || "Les valeurs ne correspondent pas.";
  }
}

export default ValidationService;
