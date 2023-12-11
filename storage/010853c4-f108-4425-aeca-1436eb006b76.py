from opentrons import protocol_api
# Metadata
metadata = {
    'protocolName': 'DNA Extraction Prep',
    'author': 'Your Name <your.email@example.com>',
    'description': 'Simple transfer of reagents for DNA extraction preparation',
    'apiLevel': '2.13'
}
def run(protocol: protocol_api.ProtocolContext):
    # Labware Setup
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '1')
    tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '2')
    source_rack_50ml = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', '7')
    source_rack_1_5ml = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '5')
    destination_rack_1_5ml = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', '3')
    # Pipette Setup
    p20_single = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])
    p300_single = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_300ul])
    # Commands
    # Transfer 50 uL of reagent from source 50ml tube to destination 1.5ml tubes
    for column in destination_rack_1_5ml.columns()[:2]:  # First 2 columns
        p300_single.pick_up_tip()
        p300_single.aspirate(50, source_rack_50ml.wells_by_name()['A1'])
        for well in column:
            p300_single.dispense(50, well)
        p300_single.drop_tip()
    # Transfer 10 uL of reagent from source 1.5ml tubes to destination 1.5ml tubes
    for source_well, dest_well in zip(source_rack_1_5ml.columns()[:2], destination_rack_1_5ml.columns()[:2]):
        for s_well, d_well in zip(source_well, dest_well):
            p20_single.pick_up_tip()
            p20_single.aspirate(10, s_well)
            p20_single.dispense(10, d_well)
            p20_single.drop_tip()
