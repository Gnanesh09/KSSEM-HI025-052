# GreenChain Payment Section - Insurance Claim Processing System
# Based on AGRI-Project: Decentralized Agricultural Data Platform

from datetime import datetime
from typing import Dict, Optional
import json


def step_by_step_payment_calculation(farmer_info: Dict, claim_info: Dict) -> Dict:
    """
    Complete payment calculation with step-by-step breakdown returned as dictionary
    
    Parameters:
    - farmer_info: Dictionary with farmer details (farmer_id, name, phone, land_area_hectares, district, crop_type, verified_harvests)
    - claim_info: Dictionary with claim and NDVI data (claim_id, insured_amount, damage_type, ndvi_pre_disaster, ndvi_post_disaster, weather_event_verified)
    
    Returns:
    - Dictionary with complete step-by-step calculation including:
        - calculation_steps: All 9 steps with formulas and values
        - farmer_details: Complete farmer information
        - claim_details: Insurance claim data
        - payment_summary: Final payment breakdown
    """
    
    result = {
        'calculation_steps': {},
        'farmer_details': {},
        'claim_details': {},
        'payment_summary': {}
    }
    
    # Store farmer details
    result['farmer_details'] = {
        'farmer_id': farmer_info['farmer_id'],
        'name': farmer_info['name'],
        'phone': farmer_info['phone'],
        'land_area_hectares': farmer_info['land_area_hectares'],
        'district': farmer_info['district'],
        'crop_type': farmer_info['crop_type'],
        'verified_harvests': farmer_info.get('verified_harvests', 0)
    }
    
    # Store claim details
    result['claim_details'] = {
        'claim_id': claim_info['claim_id'],
        'insured_amount': claim_info['insured_amount'],
        'damage_type': claim_info['damage_type'],
        'ndvi_pre_disaster': claim_info['ndvi_pre_disaster'],
        'ndvi_post_disaster': claim_info['ndvi_post_disaster'],
        'weather_event_verified': claim_info['weather_event_verified']
    }
    
    # STEP 1: Calculate NDVI Drop
    ndvi_pre = claim_info['ndvi_pre_disaster']
    ndvi_post = claim_info['ndvi_post_disaster']
    ndvi_drop = ndvi_pre - ndvi_post
    ndvi_drop_percentage = (ndvi_drop / ndvi_pre) * 100 if ndvi_pre > 0 else 0
    
    result['calculation_steps']['step_1_ndvi_calculation'] = {
        'description': 'Calculate NDVI drop to measure crop damage',
        'formula': 'NDVI Drop = Pre-Disaster NDVI - Post-Disaster NDVI',
        'ndvi_pre_disaster': ndvi_pre,
        'ndvi_post_disaster': ndvi_post,
        'ndvi_drop_absolute': round(ndvi_drop, 4),
        'ndvi_drop_percentage': round(ndvi_drop_percentage, 2),
        'interpretation': f'Crop health declined by {round(ndvi_drop_percentage, 2)}%'
    }
    
    # STEP 2: Determine Damage Severity
    if ndvi_drop_percentage >= 75:
        damage_severity = "SEVERE"
        damage_multiplier = 1.0
    elif ndvi_drop_percentage >= 50:
        damage_severity = "MAJOR"
        damage_multiplier = 0.85
    elif ndvi_drop_percentage >= 30:
        damage_severity = "MODERATE"
        damage_multiplier = 0.60
    elif ndvi_drop_percentage >= 15:
        damage_severity = "MINOR"
        damage_multiplier = 0.35
    else:
        damage_severity = "NEGLIGIBLE"
        damage_multiplier = 0.0
    
    result['calculation_steps']['step_2_damage_assessment'] = {
        'description': 'Assess damage severity based on NDVI drop percentage',
        'ndvi_drop_percentage': round(ndvi_drop_percentage, 2),
        'damage_severity': damage_severity,
        'damage_multiplier': damage_multiplier,
        'severity_thresholds': {
            'SEVERE': '≥75% drop → 100% payout',
            'MAJOR': '≥50% drop → 85% payout',
            'MODERATE': '≥30% drop → 60% payout',
            'MINOR': '≥15% drop → 35% payout',
            'NEGLIGIBLE': '<15% drop → 0% payout'
        },
        'result': f'{damage_severity} damage qualifies for {damage_multiplier:.0%} payout'
    }
    
    # STEP 3: Calculate Base Payment
    insured_amount = claim_info['insured_amount']
    base_payment = insured_amount * damage_multiplier
    
    result['calculation_steps']['step_3_base_payment'] = {
        'description': 'Calculate base payment using damage multiplier',
        'formula': 'Base Payment = Insured Amount × Damage Multiplier',
        'insured_amount': insured_amount,
        'damage_multiplier': damage_multiplier,
        'base_payment': round(base_payment, 2),
        'calculation': f'₹{insured_amount:,.2f} × {damage_multiplier:.2f} = ₹{base_payment:,.2f}'
    }
    
    # STEP 4: Calculate Weather Verification Bonus
    weather_verified = claim_info['weather_event_verified']
    weather_bonus = 0.10 if weather_verified else 0.0
    weather_bonus_amount = base_payment * weather_bonus
    
    result['calculation_steps']['step_4_weather_bonus'] = {
        'description': 'Add bonus if weather event is verified by meteorological data',
        'weather_verified': weather_verified,
        'weather_bonus_percentage': weather_bonus,
        'weather_bonus_amount': round(weather_bonus_amount, 2),
        'logic': 'If verified weather event → Add 10% bonus',
        'result': f'Weather bonus: {weather_bonus:.0%} = ₹{weather_bonus_amount:,.2f}'
    }
    
    # STEP 5: Calculate Reputation Bonus
    verified_harvests = farmer_info.get('verified_harvests', 0)
    reputation_bonus = 0.05 if verified_harvests >= 5 else 0.0
    reputation_bonus_amount = base_payment * reputation_bonus
    
    result['calculation_steps']['step_5_reputation_bonus'] = {
        'description': 'Reward farmers with verified history',
        'verified_harvests': verified_harvests,
        'reputation_bonus_percentage': reputation_bonus,
        'reputation_bonus_amount': round(reputation_bonus_amount, 2),
        'logic': 'If verified_harvests ≥ 5 → Add 5% bonus',
        'result': f'Reputation bonus: {reputation_bonus:.0%} = ₹{reputation_bonus_amount:,.2f}'
    }
    
    # STEP 6: Calculate Total with Bonuses
    total_bonus_multiplier = 1 + weather_bonus + reputation_bonus
    final_payment = base_payment * total_bonus_multiplier
    
    result['calculation_steps']['step_6_total_with_bonuses'] = {
        'description': 'Apply all bonuses to base payment',
        'formula': 'Final Payment = Base Payment × (1 + Weather Bonus + Reputation Bonus)',
        'base_payment': round(base_payment, 2),
        'weather_bonus': weather_bonus,
        'reputation_bonus': reputation_bonus,
        'total_bonus_multiplier': round(total_bonus_multiplier, 3),
        'final_payment': round(final_payment, 2),
        'calculation_breakdown': {
            'base': f'₹{base_payment:,.2f}',
            'weather_bonus': f'+₹{weather_bonus_amount:,.2f}',
            'reputation_bonus': f'+₹{reputation_bonus_amount:,.2f}',
            'total': f'₹{final_payment:,.2f}'
        }
    }
    
    # STEP 7: Apply Processing Fee
    processing_fee = 0.01 if final_payment > 0 else 0
    net_payment = final_payment - processing_fee
    
    result['calculation_steps']['step_7_processing_fee'] = {
        'description': 'Deduct blockchain transaction fee (Polygon network)',
        'final_payment': round(final_payment, 2),
        'processing_fee': processing_fee,
        'net_payment': round(net_payment, 2),
        'calculation': f'₹{final_payment:,.2f} - ₹{processing_fee} = ₹{net_payment:,.2f}'
    }
    
    # STEP 8: Determine Claim Status
    if ndvi_drop_percentage >= 50 and weather_verified:
        claim_status = "AUTO_APPROVED"
        approval_type = "SMART_CONTRACT"
    elif ndvi_drop_percentage >= 15:
        claim_status = "MANUAL_REVIEW_REQUIRED"
        approval_type = "PENDING_VALIDATION"
    else:
        claim_status = "REJECTED"
        approval_type = "INSUFFICIENT_DAMAGE"
        net_payment = 0
    
    result['calculation_steps']['step_8_approval_status'] = {
        'description': 'Determine if claim qualifies for automatic approval',
        'logic': {
            'auto_approve': 'NDVI drop ≥50% AND weather verified',
            'manual_review': 'NDVI drop between 15-50%',
            'reject': 'NDVI drop <15%'
        },
        'ndvi_drop_percentage': round(ndvi_drop_percentage, 2),
        'weather_verified': weather_verified,
        'claim_status': claim_status,
        'approval_type': approval_type,
        'result': f'Claim {claim_status} via {approval_type}'
    }
    
    # STEP 9: Generate Payment Summary
    result['payment_summary'] = {
        'claim_id': claim_info['claim_id'],
        'farmer_id': farmer_info['farmer_id'],
        'farmer_name': farmer_info['name'],
        'claim_status': claim_status,
        'approval_type': approval_type,
        'insured_amount': insured_amount,
        'damage_severity': damage_severity,
        'damage_percentage': round(ndvi_drop_percentage, 2),
        'base_payment': round(base_payment, 2),
        'total_bonuses': round(weather_bonus_amount + reputation_bonus_amount, 2),
        'final_payment': round(final_payment, 2),
        'processing_fee': processing_fee,
        'net_payment_amount': round(net_payment, 2),
        'calculation_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'blockchain_ready': True
    }
    
    return result


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    
    # Example 1: Severe Flood Damage Case
    print("\n" + "="*70)
    print("EXAMPLE 1: SEVERE FLOOD DAMAGE")
    print("="*70)
    
    farmer1 = {
        'farmer_id': 'FRM001234',
        'name': 'Rajesh Kumar',
        'phone': '+91-9876543210',
        'land_area_hectares': 2.5,
        'district': 'Mysuru',
        'crop_type': 'Rice',
        'verified_harvests': 6
    }
    
    claim1 = {
        'claim_id': 'CLM2025001',
        'insured_amount': 50000.00,
        'damage_type': 'Flood Damage',
        'ndvi_pre_disaster': 0.75,
        'ndvi_post_disaster': 0.28,
        'weather_event_verified': True
    }
    
    result1 = step_by_step_payment_calculation(farmer1, claim1)
    print(json.dumps(result1, indent=2))
    
    # Example 2: Moderate Drought Damage Case
    print("\n\n" + "="*70)
    print("EXAMPLE 2: MODERATE DROUGHT DAMAGE")
    print("="*70)
    
    farmer2 = {
        'farmer_id': 'FRM005678',
        'name': 'Lakshmi Devi',
        'phone': '+91-9123456789',
        'land_area_hectares': 1.8,
        'district': 'Tumkur',
        'crop_type': 'Cotton',
        'verified_harvests': 3
    }
    
    claim2 = {
        'claim_id': 'CLM2025002',
        'insured_amount': 75000.00,
        'damage_type': 'Drought Damage',
        'ndvi_pre_disaster': 0.68,
        'ndvi_post_disaster': 0.45,
        'weather_event_verified': True
    }
    
    result2 = step_by_step_payment_calculation(farmer2, claim2)
    print(json.dumps(result2, indent=2))
    
    # Quick Access Examples
    print("\n\n" + "="*70)
    print("ACCESSING SPECIFIC VALUES FROM DICTIONARY")
    print("="*70)
    print(f"\nFarmer 1 Net Payment: ₹{result1['payment_summary']['net_payment_amount']:,.2f}")
    print(f"Farmer 1 Status: {result1['payment_summary']['claim_status']}")
    print(f"\nFarmer 2 Net Payment: ₹{result2['payment_summary']['net_payment_amount']:,.2f}")
    print(f"Farmer 2 Status: {result2['payment_summary']['claim_status']}")
    print(f"\nStep 1 NDVI Drop (Farmer 1): {result1['calculation_steps']['step_1_ndvi_calculation']['ndvi_drop_percentage']}%")
    print(f"Step 2 Damage Severity (Farmer 1): {result1['calculation_steps']['step_2_damage_assessment']['damage_severity']}")
