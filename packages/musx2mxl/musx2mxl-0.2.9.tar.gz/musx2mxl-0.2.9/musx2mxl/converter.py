import math
from datetime import date
from io import BytesIO
from lxml.etree import Element, SubElement, parse, ElementTree, XMLSyntaxError
from musx2mxl.helper import calculate_mode_and_key_fifths, calculate_type_and_dots, calculate_step_alter_and_octave, \
    translate_clef_sign, translate_bar_style, replace_music_symbols, remove_styling_tags, translate_dynamics, \
    count_tuplet, translate_articualtion, translate_tempo_marks, calculate_transpose, translate_instrument, \
    reorder_children, find_nth_syllabic, translate_chord_suffix, translate_chord_step
import musx2mxl

ns = {"f": "http://www.makemusic.com/2012/finale"}
ns2 = {"m": "http://www.makemusic.com/2012/NotationMetadata"}
DIVISIONS = 16  # nb devisions per quarter note

VERBOSE = False

# Finale Bracket Styles
THICK_LINE = '1'
BRACKET_STRAIGHT_HOOKS = '2'
PIANO_BRACE = '3'
BRACKET_CURVED_HOOKS = '6'
DESK_BRACKET = '8'


def convert_from_stream(input_stream, metadata_stream, output_stream):
    """
    Convert data from an input stream and return the converted data as a bytes object.
    """
    tree = parse(input_stream)

    try:
        meta_tree = parse(metadata_stream)
    except XMLSyntaxError as e:
        # try to solve wrong encoding
        metadata_stream = BytesIO(metadata_stream.getvalue().decode("latin1").encode("utf-8"))
        meta_tree = parse(metadata_stream)

    output_tree = convert_tree(tree, meta_tree)

    doctype = '-//Recordare//DTD MusicXML 4.0 Partwise//EN'
    dtd_url = 'http://www.musicxml.org/dtds/partwise.dtd'

    output_tree.write(output_stream, pretty_print=True, encoding="UTF-8", xml_declaration=True,
                      doctype=f'<!DOCTYPE score-partwise PUBLIC "{doctype}" "{dtd_url}">')


def lookup_note_alter(root, entnum: str):
    noteAlters = root.xpath(f"/f:finale/f:details/f:noteAlter[@entnum = '{entnum}'][f:noteID]", namespaces=ns)
    noteAlter_map = {}
    for noteAlter in noteAlters:
        noteID = noteAlter.find("f:noteID", namespaces=ns).text
        enharmonic = noteAlter.find("f:enharmonic", namespaces=ns) is not None
        percent = noteAlter.find("f:percent", namespaces=ns) if noteAlter.find("f:percent",
                                                                               namespaces=ns) is not None else None
        noteAlter_map[noteID] = {"enharmonic": enharmonic, "percent": percent}
    return noteAlter_map


def lookup_meas_expressions(root, meas_spec_cmper: str):
    expressions = []
    measExprAssigns = root.xpath(f"/f:finale/f:others/f:measExprAssign[@cmper='{meas_spec_cmper}'][f:textExprID]",
                                 namespaces=ns)
    for measExprAssign in measExprAssigns:
        textExprID = measExprAssign.find("f:textExprID", namespaces=ns).text
        staffAssign = measExprAssign.find("f:staffAssign", namespaces=ns).text
        horzEduOff = measExprAssign.find("f:horzEduOff", namespaces=ns).text if measExprAssign.find("f:horzEduOff",
                                                                                                    namespaces=ns) is not None else None
        textExprDef = root.find(f"f:others/f:textExprDef[@cmper='{textExprID}']", namespaces=ns)
        textIDKey = textExprDef.find("f:textIDKey", namespaces=ns).text
        vertMeasExprAlign = textExprDef.find("f:vertMeasExprAlign", namespaces=ns).text if textExprDef.find(
            "f:vertMeasExprAlign", namespaces=ns) is not None else None
        categoryID = textExprDef.find("f:categoryID", namespaces=ns).text
        value = textExprDef.find("f:value", namespaces=ns).text if textExprDef.find("f:value",
                                                                                    namespaces=ns) is not None else None
        descStr = textExprDef.find("f:descStr", namespaces=ns).text if textExprDef.find("f:descStr",
                                                                                        namespaces=ns) is not None else None
        textBlock = root.find(f"f:others/f:textBlock[@cmper='{textIDKey}']", namespaces=ns)
        expression_text = None
        if textBlock is not None:
            markingsCategory = \
                root.xpath(f"/f:finale/f:others/f:markingsCategory[@cmper='{categoryID}']", namespaces=ns)[0]
            textID = textBlock.find("f:textID", namespaces=ns).text
            textTag = textBlock.find("f:textTag", namespaces=ns).text
            showShape = textBlock.find("f:textTag", namespaces=ns) is not None
            categoryType = markingsCategory.find("f:categoryType", namespaces=ns).text
            expression_text = root.find(f"f:texts/f:expression[@number='{textID}']", namespaces=ns).text if root.find(
                f"f:texts/f:expression[@number='{textID}']", namespaces=ns) is not None else None
        else:
            print(f'textBlock with cmper {textIDKey} not found.')

        if expression_text:
            # todo what if expression_text is not found
            expression = {
                "staffAssign": staffAssign,
                "horzEduOff": horzEduOff,
                "value": value,
                "categoryType": categoryType,
                "vertMeasExprAlign": vertMeasExprAlign,
                "textTag": textTag,
                "showShape": showShape,
                "descStr": descStr,
                "text": expression_text,
            }
            expressions.append(expression)
    return expressions


def lookup_txt_repeats(root, meas_spec_cmper):
    textRepeatAssigns = root.xpath(f"/f:finale/f:others/f:textRepeatAssign[@cmper='{meas_spec_cmper}']", namespaces=ns)
    txt_repeats = []
    for textRepeatAssign in textRepeatAssigns:
        topStaffOnly = textRepeatAssign.find("f:topStaffOnly", namespaces=ns) is not None
        staffList = textRepeatAssign.find("f:staffList", namespaces=ns).text if textRepeatAssign.find(
            "f:staffList", namespaces=ns) is not None else None
        horzPos = textRepeatAssign.find("f:horzPos", namespaces=ns).text if textRepeatAssign.find("f:horzPos",
                                                                                                  namespaces=ns) is not None else None
        vertPos = textRepeatAssign.find("f:vertPos", namespaces=ns).text if textRepeatAssign.find("f:vertPos",
                                                                                                  namespaces=ns) is not None else None
        repnum = textRepeatAssign.find('f:repnum', namespaces=ns).text if textRepeatAssign.find("f:repnum",
                                                                                                namespaces=ns) is not None else None
        # todo hanlde textRepeatDef
        # textRepeatDef = root.find(f"f:others/f:textRepeatDef[@cmper='{repnum}']", namespaces=ns)

        if repnum is not None:
            textRepeatText = root.find(f"f:others/f:textRepeatText[@cmper='{repnum}']", namespaces=ns)
            if textRepeatText is not None:
                rptText = textRepeatText.find('f:rptText', namespaces=ns).text if textRepeatText.find("f:rptText",
                                                                                                      namespaces=ns) is not None else None
                txt_repeats.append(
                    {'topStaffOnly': topStaffOnly, 'staffList': staffList, 'horzPos': horzPos, 'vertPos': vertPos,
                     'rptText': rptText})
            else:
                print(f'textRepeatText with cmper {repnum} not found.')

    return txt_repeats


#     textRepeatDef cmper

def lookup_meas_smart_shapes(root, meas_spec_cmper):
    smartShapeMeasMarks = root.xpath(f"/f:finale/f:others/f:smartShapeMeasMark[@cmper='{meas_spec_cmper}']",
                                     namespaces=ns)
    meas_smart_shapes = []
    for smartShapeMeasMark in smartShapeMeasMarks:
        shapeNum = smartShapeMeasMark.find('f:shapeNum', namespaces=ns).text
        smartShape = root.find(f"f:others/f:smartShape[@cmper = '{shapeNum}']", namespaces=ns)
        if smartShape is None:
            print(f'smartShape with cmper {shapeNum} not found')
        else:
            shapeType = smartShape.find("f:shapeType", namespaces=ns).text if smartShape.find("f:shapeType",
                                                                                              namespaces=ns) is not None else None
            startMeas = smartShape.find("f:startTermSeg/f:endPt/f:meas", namespaces=ns).text
            startInst = smartShape.find("f:startTermSeg/f:endPt/f:inst", namespaces=ns).text
            startEdu = smartShape.find("f:startTermSeg/f:endPt/f:edu", namespaces=ns).text if smartShape.find(
                "f:startTermSeg/f:endPt/f:edu", namespaces=ns) is not None else None
            startEntry = smartShape.find("f:startTermSeg/f:endPt/f:entryNum", namespaces=ns).text if smartShape.find(
                "f:startTermSeg/f:endPt/f:entryNum", namespaces=ns) is not None else None
            endMeas = smartShape.find("f:endTermSeg/f:endPt/f:meas", namespaces=ns).text
            endEntry = smartShape.find("f:endTermSeg/f:endPt/f:entryNum", namespaces=ns).text if smartShape.find(
                "f:endTermSeg/f:endPt/f:entryNum", namespaces=ns) is not None else None
            endInst = smartShape.find("f:endTermSeg/f:endPt/f:inst", namespaces=ns).text
            endEdu = smartShape.find("f:endTermSeg/f:endPt/f:edu", namespaces=ns).text if smartShape.find(
                "f:endTermSeg/f:endPt/f:edu", namespaces=ns) is not None else None
            meas_smart_shapes.append(
                {'shapeType': shapeType, 'startMeas': startMeas, 'startEntry': startEntry, 'startInst': startInst,
                 'endMeas': endMeas, 'startEdu': startEdu, 'endEntry': endEntry, 'endInst': endInst, 'endEdu': endEdu})
    return meas_smart_shapes


def lookup_block_text(root, id):
    textBlock = root.xpath(f"/f:finale/f:others/f:textBlock[@cmper='{id}']", namespaces=ns)[0]
    textID = textBlock.find("f:textID", namespaces=ns).text
    text = root.xpath(f"/f:finale/f:texts/f:blockText[@number='{textID}']", namespaces=ns)[0].text
    if text:
        return replace_music_symbols(remove_styling_tags(text))
    else:
        print(f"blockText with number {textID} not found.")
        return ''


def lookup_suffix(root, suffix_cmper):
    suffix_str = ""
    if suffix_cmper:
        chordAssigns = root.xpath(f"/f:finale/f:others/f:chordSuffix[@cmper='{suffix_cmper}'][f:suffix]", namespaces=ns)
        for chordAssign in chordAssigns:
            suffix = chordAssign.find("f:suffix", namespaces=ns).text
            if suffix == '209':
                suffix_str += 'b'
            elif int(suffix) >= 20:
                suffix_str += chr(int(suffix))
            else:
                suffix_str += str(suffix)

    return suffix_str


def lookup_chords(root, staff_spec_cmper, meas_spec_cmper):
    chordAssigns = root.xpath(
        f"/f:finale/f:details/f:chordAssign[@cmper1='{staff_spec_cmper}' and @cmper2='{meas_spec_cmper}']",
        namespaces=ns)
    chords = []
    for chordAssign in chordAssigns:
        rootScaleNum = chordAssign.find("f:rootScaleNum", namespaces=ns).text if chordAssign.find("f:rootScaleNum",
                                                                                                  namespaces=ns) is not None else None
        rootAlter = chordAssign.find("f:rootAlter", namespaces=ns).text if chordAssign.find("f:rootAlter",
                                                                                            namespaces=ns) is not None else None
        showAltBass = chordAssign.find("f:showAltBass", namespaces=ns) is not None
        bassScaleNum = chordAssign.find("f:bassScaleNum", namespaces=ns).text if chordAssign.find("f:bassScaleNum",
                                                                                                  namespaces=ns) is not None else None
        bassAlter = chordAssign.find("f:bassAlter", namespaces=ns).text if chordAssign.find("f:bassAlter",
                                                                                            namespaces=ns) is not None else None
        bassPosition = chordAssign.find("f:bassPosition", namespaces=ns).text if chordAssign.find("f:bassPosition",
                                                                                                  namespaces=ns) is not None else None
        suffix_cmper = chordAssign.find("f:suffix", namespaces=ns).text if chordAssign.find("f:suffix",
                                                                                            namespaces=ns) is not None else None
        horzEdu = chordAssign.find("f:horzEdu", namespaces=ns).text if chordAssign.find("f:horzEdu",
                                                                                        namespaces=ns) is not None else None
        suffix_text = lookup_suffix(root, suffix_cmper)

        if suffix_text == "es":
            suffix_text = ""
            rootAlter = "-1"
        if suffix_text == "is":
            suffix_text = ""
            rootAlter = "1"

        chords.append(
            {'rootScaleNum': rootScaleNum, 'rootAlter': rootAlter, 'showAltBass': showAltBass,
             'bassScaleNum': bassScaleNum, 'bassAlter': bassAlter, 'bassPosition': bassPosition,
             'suffix_text': suffix_text, 'horzEdu': horzEdu})
        if VERBOSE: print(meas_spec_cmper, chords)
    return chords


def lookup_staff_groups(root):
    # todo check multiStaffInstGroup and multiStaffGroupID
    staff_group_list = []
    staff_groups = root.xpath("/f:finale/f:details/f:staffGroup[not(@part)]", namespaces=ns)
    for staffGroup in staff_groups:
        startInst = staffGroup.find("f:startInst", namespaces=ns).text
        endInst = staffGroup.find("f:endInst", namespaces=ns).text
        startMeas = staffGroup.find("f:startMeas", namespaces=ns).text
        endMeas = staffGroup.find("f:endMeas", namespaces=ns).text
        fullID_ = staffGroup.find("f:fullID", namespaces=ns)
        abbrvID_ = staffGroup.find("f:abbrvID", namespaces=ns)
        fullName = lookup_block_text(root, fullID_.text) if fullID_ is not None else None
        abbrvName = lookup_block_text(root, abbrvID_.text) if abbrvID_ is not None else None
        bracket_id = staffGroup.find("f:bracket/f:id", namespaces=ns).text if staffGroup.find("f:bracket/f:id",
                                                                                              namespaces=ns) is not None else None
        staff_group_list.append({'startInst': startInst, 'endInst': endInst, 'startMeas': startMeas, 'endMeas': endMeas,
                                 'fullName': fullName, 'abbrvName': abbrvName, 'bracket_id': bracket_id})
    if VERBOSE: print(f"staff_group_list: {staff_group_list}")
    return staff_group_list


def find_staff_group_name(param, staff_spec_cmper, staff_groups):
    names = []
    for staff_group in staff_groups:
        if int(staff_group["startInst"]) <= int(staff_spec_cmper) <= int(staff_group["endInst"]) and staff_group[
            param]:
            names.append(staff_group[param])
    return ' '.join(names) if names else None


def get_piano_brace_staff_group(staff_spec_cmper, staff_groups):
    for staff_group in staff_groups:
        if (staff_group["bracket_id"] == PIANO_BRACE and staff_group["startInst"] != staff_group["endInst"] and
                int(staff_group["startInst"]) <= int(staff_spec_cmper) <= int(staff_group["endInst"])):
            return staff_group
    return None


def convert_tree(tree, meta_tree):
    root = tree.getroot()
    score_partwise = Element("score-partwise", version="4.0")

    if meta_tree:
        meta_root = meta_tree.getroot()
        handle_meta_data(score_partwise, meta_root)
    part_list = SubElement(score_partwise, "part-list")

    timeSigDoAbrvCommon = len(
        root.xpath("/f:finale/f:options/f:timeSignatureOptions/f:timeSigDoAbrvCommon", namespaces=ns)) > 0
    timeSigDoAbrvCut = len(
        root.xpath("/f:finale/f:options/f:timeSignatureOptions/f:timeSigDoAbrvCut", namespaces=ns)) > 0

    staff_groups = lookup_staff_groups(root)

    staff_specs = root.xpath("/f:finale/f:others/f:staffSpec[@cmper != '32767']", namespaces=ns)
    i = 1
    part_ids = {}
    for staff_spec in staff_specs:
        staff_spec_cmper = staff_spec.get("cmper")
        fullName_ = staff_spec.find('f:fullName', namespaces=ns)
        abbrvName_ = staff_spec.find('f:abbrvName', namespaces=ns)
        instUuid = staff_spec.find('f:instUuid', namespaces=ns).text
        if fullName_ is not None:
            fullName = lookup_block_text(root, fullName_.text)
        else:
            fullName = find_staff_group_name('fullName', staff_spec_cmper, staff_groups)
        if abbrvName_ is not None:
            abbrvName = lookup_block_text(root, abbrvName_.text)
        else:
            abbrvName = find_staff_group_name('abbrvName', staff_spec_cmper, staff_groups)

        piano_staff_group = get_piano_brace_staff_group(staff_spec_cmper, staff_groups)
        if piano_staff_group is None or piano_staff_group['startInst'] == staff_spec_cmper:
            part_id = f"P{i}"
            i += 1
            part_ids[staff_spec_cmper] = part_id
            score_part = SubElement(part_list, "score-part", id=part_id)
            SubElement(score_part, "part-name").text = fullName if fullName else ''
            if abbrvName:
                SubElement(score_part, "part-abbreviation").text = abbrvName

            instrument_name, instrument_sound = translate_instrument(instUuid)
            if instrument_name:
                score_instrument = SubElement(score_part, "score-instrument", id=f'{part_id}-I1')
                SubElement(score_instrument, "instrument-name").text = instrument_name
                if instrument_sound: SubElement(score_instrument, "instrument-sound").text = instrument_sound

    handle_tempo = True  # todo how to handle tempo changes correctly

    for staff_spec in staff_specs:
        staff_spec_cmper = staff_spec.get("cmper")
        if staff_spec_cmper in part_ids:
            part = SubElement(score_partwise, "part", id=part_ids[staff_spec_cmper])

            piano_staff_group = get_piano_brace_staff_group(staff_spec_cmper, staff_groups)

            transp_key_adjust = int(
                staff_spec.find('f:transposition/f:keysig/f:adjust', namespaces=ns).text) if staff_spec.find(
                'f:transposition/f:keysig/f:adjust', namespaces=ns) is not None else 0
            transp_interval = int(
                staff_spec.find('f:transposition/f:keysig/f:interval', namespaces=ns).text) if staff_spec.find(
                'f:transposition/f:keysig/f:interval', namespaces=ns) is not None else 0

            current_key = -1
            current_beats = None
            current_divbeat = None
            current_clefID = None
            ending_cnt = 0  # todo how to find ending numbers correctly

            meas_specs = root.xpath("/f:finale/f:others/f:measSpec[not(@shared) and not(@part)]", namespaces=ns)
            nb_measures = len(meas_specs)
            for meas_idx, meas_spec in enumerate(meas_specs):
                meas_spec_cmper = meas_spec.get("cmper")
                if VERBOSE: print(f'Staff: {staff_spec_cmper} - Measure: {meas_spec_cmper}')
                measure = SubElement(part, "measure", number=meas_spec_cmper)
                beats = meas_spec.find("f:beats", namespaces=ns).text
                divbeat = meas_spec.find("f:divbeat", namespaces=ns).text
                key_ = meas_spec.find("f:keySig/f:key", namespaces=ns)
                barline_ = meas_spec.find("f:barline", namespaces=ns).text if meas_spec.find("f:barline",
                                                                                             namespaces=ns) is not None else 'normal'
                if meas_idx == nb_measures - 1:
                    barline_ = 'final'
                forRepBar = meas_spec.find("f:forRepBar", namespaces=ns) is not None
                bacRepBar = meas_spec.find("f:bacRepBar", namespaces=ns) is not None
                barEnding = meas_spec.find("f:barEnding", namespaces=ns) is not None
                hasSmartShape = meas_spec.find("f:hasSmartShape", namespaces=ns) is not None
                txtRepeats = meas_spec.find("f:txtRepeats", namespaces=ns) is not None
                hasChord = meas_spec.find("f:hasChord", namespaces=ns) is not None
                if txtRepeats:
                    txt_repeats = lookup_txt_repeats(root, meas_spec_cmper)
                    if VERBOSE: print(f'Measure text repeats: {txt_repeats}')
                else:
                    txt_repeats = []
                if hasSmartShape:
                    meas_smart_shapes = lookup_meas_smart_shapes(root, meas_spec_cmper)
                    if VERBOSE: print(f'Measure smart shapes: {meas_smart_shapes}')
                else:
                    meas_smart_shapes = []
                # todo: Check if inst is always referring to staff_spec_cmper
                for txt_repeat in txt_repeats:
                    if (txt_repeat['topStaffOnly'] and staff_spec_cmper == '1') or txt_repeat[
                        'staffList'] == staff_spec_cmper:
                        # todo horzPos vertPos (EVPU 288 per inch) relative-x relative-y (tenth of a staff space)
                        if txt_repeat['rptText'] == '%':
                            direction = SubElement(measure, "direction", placement='above')
                            direction_type = SubElement(direction, "direction-type")
                            SubElement(direction_type, "segno")
                        elif txt_repeat['rptText'] == 'Þ':
                            direction = SubElement(measure, "direction", placement='above')
                            direction_type = SubElement(direction, "direction-type")
                            SubElement(direction_type, "coda")
                        else:
                            direction = SubElement(measure, "direction", placement='below')
                            direction_type = SubElement(direction, "direction-type")
                            SubElement(direction_type, "words").text = txt_repeat['rptText']

                for meas_smart_shape in meas_smart_shapes:
                    if meas_smart_shape['shapeType'] == 'cresc':
                        if meas_smart_shape['startMeas'] == meas_spec_cmper and meas_smart_shape[
                            'startInst'] == staff_spec_cmper:

                            direction = SubElement(measure, "direction", placement='below')
                            direction_type = SubElement(direction, "direction-type")
                            if meas_smart_shape['startEdu']:
                                SubElement(direction, "offset").text = str(
                                    math.ceil((int(meas_smart_shape['startEdu']) * DIVISIONS) / 1024))
                            SubElement(direction_type, "wedge", type="crescendo")
                        if meas_smart_shape['endMeas'] == meas_spec_cmper and meas_smart_shape[
                            'startInst'] == staff_spec_cmper:

                            direction = SubElement(measure, "direction", placement='below')
                            direction_type = SubElement(direction, "direction-type")
                            if meas_smart_shape['endEdu']:
                                SubElement(direction, "offset").text = str(
                                    math.ceil((int(meas_smart_shape['endEdu']) * DIVISIONS) / 1024))
                            # if staff_id:
                            #     SubElement(direction, "staff").text = str(staff_id)
                            SubElement(direction_type, "wedge", type="stop")
                    elif meas_smart_shape['shapeType'] == 'decresc':
                        if meas_smart_shape['startMeas'] == meas_spec_cmper and meas_smart_shape[
                            'endInst'] == staff_spec_cmper:

                            direction = SubElement(measure, "direction", placement='below')
                            direction_type = SubElement(direction, "direction-type")
                            if meas_smart_shape['startEdu']:
                                SubElement(direction, "offset").text = str(
                                    math.ceil((int(meas_smart_shape['startEdu']) * DIVISIONS) / 1024))
                            SubElement(direction_type, "wedge", type="diminuendo")

                        if meas_smart_shape['endMeas'] == meas_spec_cmper and meas_smart_shape[
                            'endInst'] == staff_spec_cmper:

                            direction = SubElement(measure, "direction", placement='below')
                            direction_type = SubElement(direction, "direction-type")
                            if meas_smart_shape['endEdu']:
                                SubElement(direction, "offset").text = str(
                                    math.ceil((int(meas_smart_shape['endEdu']) * DIVISIONS) / 1024))
                            # if staff_id:
                            #     SubElement(direction, "staff").text = str(staff_id)
                            SubElement(direction_type, "wedge", type="stop")
                    elif meas_smart_shape['shapeType'] == 'octaveUp':
                        pass
                    elif meas_smart_shape['shapeType'] == 'octaveDown':
                        pass
                    elif meas_smart_shape['shapeType'] == 'slurUp':
                        pass
                    elif meas_smart_shape['shapeType'] == 'trill':
                        pass
                    elif meas_smart_shape['shapeType'] == 'smartLine':
                        pass
                    elif meas_smart_shape['shapeType'] == 'dashLine':
                        pass
                    elif meas_smart_shape['shapeType'] == 'trillExt':
                        pass
                    elif meas_smart_shape['shapeType'] == 'solidLine':
                        pass
                    else:
                        if meas_smart_shape['startEntry'] is None:
                            print(meas_smart_shape)

                leftBarline = meas_spec.find("f:leftBarline", namespaces=ns).text
                if key_ is None:
                    key = None
                else:
                    key = int(key_.text)

                attributes = None
                if (meas_idx == 0):
                    attributes = handle_devisions(measure)
                if key != current_key:
                    attributes = handle_key_change(measure, attributes, key, transp_key_adjust, transp_interval)
                    current_key = key

                if beats != current_beats or divbeat != current_divbeat:
                    attributes = handle_time_change(measure, attributes, beats, divbeat, timeSigDoAbrvCommon,
                                                    timeSigDoAbrvCut)
                    current_beats = beats
                    current_divbeat = divbeat

                if forRepBar or barEnding:
                    left_barline = SubElement(measure, "barline", location='left')
                    if barEnding:
                        ending_cnt += 1
                        SubElement(left_barline, "ending", number=str(ending_cnt), type='start').text = f'{ending_cnt}.'
                    if forRepBar:
                        SubElement(left_barline, "bar-style").text = 'heavy-light'
                        SubElement(left_barline, "repeat", direction='forward')

                if piano_staff_group:
                    staff_id = 1
                    clefIDs = {}
                    prev = False
                    piano_staffs = [staff_spec.get("cmper") for staff_spec in staff_specs if
                                    int(piano_staff_group["startInst"]) <= int(staff_spec.get("cmper")) <= int(
                                        piano_staff_group["endInst"])]
                    for piano_staff_spec_cmper in piano_staffs:
                        if prev:
                            backup = SubElement(measure, "backup")
                            # todo is duration correctly calculated? Always start from start measure?
                            SubElement(backup, "duration").text = str(
                                (int(current_beats) * int(current_divbeat) * DIVISIONS) // 1024)

                        if hasChord:
                            chords = lookup_chords(root, piano_staff_spec_cmper, meas_spec_cmper)
                            handle_chords(measure, chords, key, transp_key_adjust, staff_id)

                        clefID, handle_tempo = process_gfholds(piano_staff_spec_cmper, meas_spec_cmper, staff_id,
                                                               measure, root, meas_spec,
                                                               handle_tempo, barline_,
                                                               bacRepBar, barEnding, ending_cnt,
                                                               current_beats, current_divbeat, key,
                                                               transp_key_adjust, transp_interval)
                        clefIDs[staff_id] = clefID
                        staff_id += 1
                        prev = True
                    if clefIDs != current_clefID:
                        attributes = handle_mutli_staff_cleff_change(root, measure, attributes, clefIDs)
                        current_clefID = clefIDs
                else:
                    if hasChord:
                        chords = lookup_chords(root, staff_spec_cmper, meas_spec_cmper)
                        handle_chords(measure, chords, key, transp_key_adjust, 1)

                    clefID, handle_tempo = process_gfholds(staff_spec_cmper, meas_spec_cmper, None, measure,
                                                           root, meas_spec, handle_tempo, barline_, bacRepBar,
                                                           barEnding, ending_cnt, current_beats, current_divbeat, key,
                                                           transp_key_adjust, transp_interval)
                    # todo handle clefListID =(mid-measure clef changes)
                    # todo use <hasExpr/> to determine show time_signature
                    # todo use <showClefFirstSystemOnly/> to determine show clef
                    if clefID != current_clefID:
                        attributes = handle_clef_change(root, measure, attributes, clefID)
                        current_clefID = clefID

                if attributes is not None:
                    reorder_children(attributes,
                                     ['footnote', 'level', 'divisions', 'key', 'time', 'staves', 'part-symbol',
                                      'instruments', 'clef', 'staff-details', 'transpose', 'for-part', 'directive',
                                      'measure-style'])
    return ElementTree(score_partwise)


# default-x="616.935484" default-y="1511.049022" justify="center" valign="top" font-size="22"
def add_credit(score_partwise, page, credit_type, credit_words, default_x, default_y, justify, valign, font_size):
    credit = SubElement(score_partwise, "credit", page=str(page))
    credit_type_ = SubElement(credit, "credit-type")
    credit_type_.text = credit_type
    credit_words_ = SubElement(credit, "credit-words")
    credit_words_.set('default-x', str(default_x))
    credit_words_.set('default-y', str(default_y))
    credit_words_.set('justify', justify)
    credit_words_.set('valign', valign)
    credit_words_.set('font-size', str(font_size))
    credit_words_.text = credit_words


def handle_meta_data(score_partwise, meta_root):
    identification = SubElement(score_partwise, "identification")
    encoding = SubElement(identification, "encoding")
    SubElement(encoding, "software").text = "musx2mxl " + musx2mxl.__version__
    SubElement(encoding, "encoding-date").text = date.today().strftime("%Y-%m-%d")

    title = meta_root.xpath("/m:metadata/m:fileInfo/m:title", namespaces=ns2)[0] if meta_root.xpath(
        "/m:metadata/m:fileInfo/m:title", namespaces=ns2) else None
    if title is not None:
        add_credit(score_partwise, 1, 'title', title.text, 616.935484, 1511.049022, 'center', 'top', 22)
    subtitle = meta_root.xpath("/m:metadata/m:fileInfo/m:subtitle", namespaces=ns2)[0] if meta_root.xpath(
        "/m:metadata/m:fileInfo/m:subtitle", namespaces=ns2) else None
    if subtitle is not None:
        add_credit(score_partwise, 1, 'subtitle', subtitle.text, 616.935484, 1453.898908, 'center', 'top', 14)
    composer = meta_root.xpath("/m:metadata/m:fileInfo/m:composer", namespaces=ns2)[0] if meta_root.xpath(
        "/m:metadata/m:fileInfo/m:composer", namespaces=ns2) else None
    if composer is not None:
        add_credit(score_partwise, 1, 'composer', composer.text, 1148.145796, 1411.049022, 'right', 'bottom', 10)


def handle_devisions(measure):
    attributes = SubElement(measure, "attributes")
    divisions = SubElement(attributes, "divisions")
    divisions.text = str(DIVISIONS)

    return attributes


def lookup_clef_info(root, clefID: str):
    if clefID:
        clef_def = root.find(f"f:options/f:clefOptions/f:clefDef[@index = '{clefID}']", namespaces=ns)
        clef_char = clef_def.find('f:clefChar', namespaces=ns)
        clef_char_ = clef_char.text if clef_char is not None else None
        # todo what if shape instead of clef_char (example : TAB)
        sign, clef_octave_change = translate_clef_sign(clef_char_)
        clef_y_disp = clef_def.find('f:clefYDisp', namespaces=ns)
        clef_y_disp_ = int(clef_y_disp.text) if clef_y_disp is not None else 0
        line = str(5 + clef_y_disp_ // 2)
        return {'sign': sign, 'line': line, 'clef_octave_change': str(clef_octave_change)}
    else:
        return {'sign': 'G', 'line': '2', 'clef_octave_change': '0'}


def handle_mutli_staff_cleff_change(root, measure, attributes, clefIDs):
    if attributes is None:
        attributes = SubElement(measure, "attributes")
    for staff_id, clefID in clefIDs.items():
        clef_info = lookup_clef_info(root, clefID)
        clef = SubElement(attributes, "clef", number=str(staff_id))
        sign = SubElement(clef, "sign")
        sign.text = clef_info['sign']
        line = SubElement(clef, "line")
        line.text = clef_info['line']
        if clef_info['clef_octave_change'] != '0':
            clef_octave_change = SubElement(clef, "clef-octave-change").text = clef_info['clef_octave_change']

    return attributes


def handle_clef_change(root, measure, attributes, clefID):
    if attributes is None:
        attributes = SubElement(measure, "attributes")

    clef_info = lookup_clef_info(root, clefID)
    clef = SubElement(attributes, "clef")
    sign = SubElement(clef, "sign")
    sign.text = clef_info['sign']
    line = SubElement(clef, "line")
    line.text = clef_info['line']
    if clef_info['clef_octave_change'] != '0':
        clef_octave_change = SubElement(clef, "clef-octave-change")
        clef_octave_change.text = clef_info['clef_octave_change']

    return attributes


def handle_chords(measure, chords, key, transp_key_adjust, staff_id):
    for chord in chords:
        suffix = translate_chord_suffix(chord['suffix_text'])
        harmony = SubElement(measure, "harmony")
        chord_root = SubElement(harmony, "root")
        step, alter = translate_chord_step(key, transp_key_adjust, chord['rootScaleNum'],
                                           chord['rootAlter'])
        SubElement(chord_root, "root-step").text = step
        if alter != 0:
            SubElement(chord_root, "root-alter").text = str(alter)
        kind = SubElement(harmony, "kind")
        kind.text = suffix["kind"]
        kind.set("use-symbols", suffix["use-symbols"])
        kind.set("parentheses-degrees", suffix["parentheses-degrees"])
        if suffix["text"]:
            kind.set("text", suffix["text"])
        if chord["showAltBass"]:
            bass = SubElement(harmony, "bass")
            if chord["bassPosition"] == "underRoot":
                bass.set("arrangement", "vertical")
            bass_step, bass_alter = translate_chord_step(key, transp_key_adjust, chord['bassScaleNum'],
                                                         chord['bassAlter'])
            SubElement(bass, "bass-step").text = str(bass_step)
            if bass_alter != 0:
                SubElement(bass, "bass-alter").text = str(bass_alter)

        for degree in suffix["degrees"]:
            degree_ = SubElement(harmony, "degree")
            SubElement(degree_, "degree-value").text = str(degree['degree-value'])
            SubElement(degree_, "degree-alter").text = str(degree['degree-alter'])
            SubElement(degree_, "degree-type").text = str(degree['degree-type'])

        if chord['horzEdu']:
            SubElement(harmony, "offset").text = str(math.ceil((int(chord['horzEdu']) * DIVISIONS) / 1024))

        if staff_id > 1:
            SubElement(harmony, "staff").text = str(staff_id)


def handle_key_change(measure, attributes, key, transp_key_adjust, transp_interval):
    mode, fifths = calculate_mode_and_key_fifths(key, transp_key_adjust)
    if attributes is None:
        attributes = SubElement(measure, "attributes")
    key_ = SubElement(attributes, "key")
    SubElement(key_, "fifths").text = str(fifths)
    SubElement(key_, "mode").text = mode
    if transp_interval:
        diatonic, chromatic, octave_change = calculate_transpose(transp_interval)
        transpose = SubElement(attributes, "transpose")
        SubElement(transpose, "diatonic").text = str(diatonic)
        SubElement(transpose, "chromatic").text = str(chromatic)
        if octave_change:
            SubElement(transpose, "octave-change").text = str(octave_change)

    return attributes


def handle_time_change(measure, attributes, beats, divbeat, timeSigDoAbrvCommon: bool, timeSigDoAbrvCut: bool):
    if attributes is None:
        attributes = SubElement(measure, "attributes")
    time_ = SubElement(attributes, "time")
    beats_ = SubElement(time_, "beats")
    beats_type = SubElement(time_, "beat-type")
    if int(divbeat) % 1536 == 0:
        beats_type.text = '8'
        beats_.text = str(int(beats) * 3 * int(divbeat) // 1536)
    elif 4096 % int(divbeat) == 0:
        beats_.text = beats
        beats_type.text = str(4096 // int(divbeat))
        if beats == '4' and divbeat == '1024' and timeSigDoAbrvCommon:
            time_.set('symbol', 'common')
        if beats == '2' and divbeat == '2048' and timeSigDoAbrvCut:
            time_.set('symbol', 'cut')
    else:
        print("Unknown divbeat {}".format(divbeat))
    return attributes


def process_frame(root, measure, frameSpec_cmper, frame_num, staff_id, key, transp_key_adjust, transp_interval):
    if staff_id is None:
        voice = frame_num
    else:
        voice = (staff_id - 1) * 4 + frame_num
    frameSpecs = root.xpath(f"/f:finale/f:others/f:frameSpec[@cmper = '{frameSpec_cmper}']", namespaces=ns)
    for frameSpec in frameSpecs:
        startEntry = frameSpec.find("f:startEntry", namespaces=ns)
        endEntry = frameSpec.find("f:endEntry", namespaces=ns)
        if (startEntry is not None) and (endEntry is not None):
            process_frame_entries(root, measure, startEntry.text, endEntry.text, staff_id, voice, key,
                                  transp_key_adjust, transp_interval, [])


def process_frame_entries(root, measure, current_entnum, end_entnum, staff_id, voice, key, transp_key_adjust,
                          transp_interval,
                          tuplet_attributes):
    current_entry = root.xpath(f"/f:finale/f:entries/f:entry[@entnum = '{current_entnum}']", namespaces=ns)[
        0] if root.xpath(f"/f:finale/f:entries/f:entry[@entnum = '{current_entnum}']", namespaces=ns) else None
    if current_entry is None:
        return
    tuplet_attributes = process_entry(root, measure, current_entry, staff_id, voice, key, transp_key_adjust,
                                      transp_interval, tuplet_attributes)

    if current_entnum != end_entnum:
        next_entnum = current_entry.get("next")
        if next_entnum:
            process_frame_entries(root, measure, next_entnum, end_entnum, staff_id, voice, key, transp_key_adjust,
                                  transp_interval,
                                  tuplet_attributes)


def handleTupletStart(root, entry, notations, tuplet_attributes):
    entnum = entry.get("entnum")
    tupletDefs = root.xpath(f"/f:finale/f:details/f:tupletDef[@entnum = '{entnum}'][f:symbolicNum]", namespaces=ns)
    if len(tuplet_attributes) == 0:
        idx = 0
    else:
        idx = max([int(tuplet_attribute['number']) for tuplet_attribute in tuplet_attributes])

    for tupletDef in tupletDefs:
        idx += 1
        number = str(idx)
        attributes = {
            'symbolicNum': tupletDef.find("f:symbolicNum", namespaces=ns).text,
            'symbolicDur': tupletDef.find("f:symbolicDur", namespaces=ns).text,
            'refNum': tupletDef.find("f:refNum", namespaces=ns).text,
            'refDur': tupletDef.find("f:refDur", namespaces=ns).text,
            'count': 0,
            'number': number,
        }
        tuplet = SubElement(notations, 'tuplet', number=number, type='start')
        if idx > 1:
            actual_type, _ = calculate_type_and_dots(int(attributes['symbolicDur']))
            normal_type, _ = calculate_type_and_dots(int(attributes['refDur']))
            tuplet_actual = SubElement(tuplet, 'tuplet-actual')
            SubElement(tuplet_actual, 'tuplet-number').text = attributes['symbolicNum']
            SubElement(tuplet_actual, 'tuplet-type').text = actual_type
            tuplet_normal = SubElement(tuplet, 'tuplet-normal')
            SubElement(tuplet_normal, 'tuplet-number').text = attributes['refNum']
            SubElement(tuplet_normal, 'tuplet-type').text = normal_type

        tuplet_attributes.append(attributes)


def handleSmartShapeDetail(root, entry, notations):
    entnum = entry.get("entnum")
    smartShapeEntryMarks = root.xpath(f"/f:finale/f:details/f:smartShapeEntryMark[@entnum = '{entnum}']", namespaces=ns)
    for smartShapeEntryMark in smartShapeEntryMarks:
        shapeNum = smartShapeEntryMark.find('f:shapeNum', namespaces=ns).text
        smartShape = root.find(f"f:others/f:smartShape[@cmper = '{shapeNum}']", namespaces=ns)
        if smartShape is not None:
            shapeType = smartShape.find("f:shapeType", namespaces=ns).text if smartShape.find("f:shapeType",
                                                                                              namespaces=ns) is not None else None
            startEntry = smartShape.find("f:startTermSeg/f:endPt/f:entryNum", namespaces=ns).text
            endEntry = smartShape.find("f:startTermSeg/f:endPt/f:entryNum", namespaces=ns).text

            if shapeType == 'slurAuto' or shapeType == 'slurUp':
                slur_type = 'start' if startEntry == entnum else 'stop'
                SubElement(notations, 'slur', number='1', type=slur_type)
        else:
            print(f'Smart shape with cmper {shapeNum} not found.')


def lookup_artic_detail(root, entnum):
    articAssigns = root.xpath(f"/f:finale/f:details/f:articAssign[@entnum = '{entnum}'][f:articDef]", namespaces=ns)
    artic_details = []
    for articAssign in articAssigns:
        articDef_cmper = articAssign.find("f:articDef", namespaces=ns).text
        articDef = root.xpath(f"/f:finale/f:others/f:articDef[@cmper = '{articDef_cmper}']", namespaces=ns)[0]
        charMain = articDef.find("f:charMain", namespaces=ns).text
        charAlt = articDef.find("f:charAlt", namespaces=ns).text
        artic_details.append({'charMain': charMain, 'charAlt': charAlt})

    return artic_details


def lookup_lyric_details(root, entnum):
    lyrDataVerseList = root.xpath(f"/f:finale/f:details/f:lyrDataVerse[@entnum = '{entnum}'][f:syll]", namespaces=ns)
    lyric_details = []
    for lyrDataVerse in lyrDataVerseList:
        lyricNumber = lyrDataVerse.find("f:lyricNumber", namespaces=ns).text
        syll = lyrDataVerse.find("f:syll", namespaces=ns).text
        verse = root.find(f"f:texts/f:verse[@number = '{lyricNumber}']", namespaces=ns).text
        if verse:
            text, syllabic, extend = find_nth_syllabic(verse, int(syll))
            lyric_details.append({'number': lyricNumber, 'syllabic': syllabic, 'extend': extend, 'text': text})
        else:
            print(f"Verse not found with number= {lyricNumber}")
    return lyric_details


def add_rest_to_empty_measure(root, measure, meas_spec_cmper, staff_id):
    first_gfhold = root.find(f"f:details/f:gfhold[@cmper2 = '{meas_spec_cmper}'][f:frame1]", namespaces=ns)
    if first_gfhold is not None:
        frame = first_gfhold.find(f"f:frame1", namespaces=ns).text
        frameSpec = root.find(f"f:others/f:frameSpec[@cmper = '{frame}'][f:startEntry][f:endEntry]", namespaces=ns)
        start_entnum = frameSpec.find("f:startEntry", namespaces=ns).text
        end_entnum = frameSpec.find("f:endEntry", namespaces=ns).text
        current_entnum = None
        next_entnum = start_entnum
        dura = 0
        while current_entnum != end_entnum:
            entry = root.find(f"f:entries/f:entry[@entnum = '{next_entnum}']", namespaces=ns)
            current_entnum = next_entnum
            next_entnum = entry.get("next")
            dura += int(entry.find("f:dura", namespaces=ns).text)

        type_name, nb_dots = calculate_type_and_dots(dura)  # todo what if dura does not match type + dots
        note = SubElement(measure, "note")
        SubElement(note, "rest")
        SubElement(note, "duration").text = str(math.ceil((dura * DIVISIONS) / 1024))
        voice = (staff_id - 1) * 4 + 1 if staff_id is not None else 1
        SubElement(note, "voice").text = str(voice)
        SubElement(note, "type").text = type_name
        for _ in range(nb_dots):
            SubElement(note, "dot")
        if staff_id:
            SubElement(note, "staff").text = str(staff_id)


def process_gfholds(staff_spec_cmper, meas_spec_cmper, staff_id, measure, root, meas_spec,
                    handle_tempo, barline_, bacRepBar, barEnding, ending_cnt, current_beats,
                    current_divbeat, key, transp_key_adjust, transp_interval):
    clefID = None
    gfholds = root.xpath(
        f"/f:finale/f:details/f:gfhold[@cmper1 = '{staff_spec_cmper}' and @cmper2 = '{meas_spec_cmper}']",
        namespaces=ns)
    if len(gfholds) == 0:
        first_clefID = root.find(f"f:details/f:gfhold[@cmper1 = '{staff_spec_cmper}']/f:clefID",
                                 namespaces=ns)
        clefID = first_clefID.text if first_clefID is not None else None
        add_rest_to_empty_measure(root, measure, meas_spec_cmper, staff_id)

    hasExpr = meas_spec.find("f:hasExpr", namespaces=ns) is not None
    if hasExpr:
        expressions = lookup_meas_expressions(root, meas_spec_cmper)
        for expression in expressions:

            # vertMeasExprAlign =  belowStaffOrEntry , aboveStaffOrEntry, manual
            placement = 'below' if expression['vertMeasExprAlign'] == 'belowStaffOrEntry' else 'above'

            if VERBOSE: print(f'Expression: {expression}')
            if expression['categoryType'] == 'misc' and expression['staffAssign'] == staff_spec_cmper:
                # check if expression is recognizes as dynamics
                dynamic_name = translate_dynamics(expression['text'])
                if dynamic_name is not None:
                    expression['categoryType'] = 'dynamics'
                else:
                    direction = SubElement(measure, "direction", placement=placement)
                    direction_type = SubElement(direction, "direction-type")
                    if expression['horzEduOff']:
                        SubElement(direction, "offset").text = str(
                            math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                    if staff_id:
                        SubElement(direction, "staff").text = str(staff_id)
                    words = SubElement(direction_type, 'words')
                    words.text = remove_styling_tags(expression['text'])
                    words.set('font-style', 'italic')
            if expression['categoryType'] == 'dynamics' and expression['staffAssign'] == staff_spec_cmper:
                dynamic_name = translate_dynamics(expression['text'])
                if dynamic_name is not None:
                    direction = SubElement(measure, "direction", placement=placement)
                    direction_type = SubElement(direction, "direction-type")
                    if expression['horzEduOff']:
                        SubElement(direction, "offset").text = str(
                            math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                    if staff_id:
                        SubElement(direction, "staff").text = str(staff_id)
                    dynamics = SubElement(direction_type, "dynamics")
                    SubElement(dynamics, dynamic_name)
            elif expression['categoryType'] == 'tempoAlts' and expression['staffAssign'] == staff_spec_cmper:
                direction = SubElement(measure, "direction", placement=placement)
                direction_type = SubElement(direction, "direction-type")
                if expression['horzEduOff']:
                    SubElement(direction, "offset").text = str(
                        math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                if staff_id:
                    SubElement(direction, "staff").text = str(staff_id)
                words = SubElement(direction_type, 'words')
                words.text = remove_styling_tags(expression['text'])
                words.set('font-style', 'italic')
            elif expression['categoryType'] == 'expressiveText' and expression['staffAssign'] == staff_spec_cmper:
                direction = SubElement(measure, "direction", placement=placement)
                direction_type = SubElement(direction, "direction-type")
                if expression['horzEduOff']:
                    SubElement(direction, "offset").text = str(
                        math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                if staff_id:
                    SubElement(direction, "staff").text = str(staff_id)
                words = SubElement(direction_type, 'words')
                words.text = remove_styling_tags(expression['text'])
                words.set('font-style', 'italic')
            elif expression['categoryType'] == 'techniqueText' and expression['staffAssign'] == staff_spec_cmper:
                direction = SubElement(measure, "direction", placement=placement)
                direction_type = SubElement(direction, "direction-type")
                if expression['horzEduOff']:
                    SubElement(direction, "offset").text = str(
                        math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                if staff_id:
                    SubElement(direction, "staff").text = str(staff_id)
                words = SubElement(direction_type, 'words')
                words.text = remove_styling_tags(expression['text'])
                words.set('font-style', 'italic')
            elif expression['categoryType'] == 'tempoMarks':
                words, beat_unit, has_dot, per_minute, parentheses = translate_tempo_marks(expression['text'])
                direction = SubElement(measure, "direction", placement=placement)
                if words:
                    direction_type = SubElement(direction, "direction-type")
                    if expression['horzEduOff']:
                        SubElement(direction, "offset").text = str(
                            math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                    SubElement(direction_type, "words").text = words
                if beat_unit and per_minute:
                    direction_type = SubElement(direction, "direction-type")
                    if expression['horzEduOff']:
                        SubElement(direction, "offset").text = str(
                            math.ceil((int(expression['horzEduOff']) * DIVISIONS) / 1024))
                    metronome = SubElement(direction_type, "metronome", parentheses=parentheses)
                    SubElement(metronome, "beat-unit").text = beat_unit
                    if has_dot:
                        SubElement(metronome, "beat-unit-dot")
                    SubElement(metronome, "per-minute").text = per_minute
            elif expression['categoryType'] == 'rehearsalMarks':
                # if not '^rehearsal()' in expression['text'] and not 'Rehearsal' in expression['descStr']:
                #     print(meas_spec_cmper, 'rehearsalMarks', expression)
                # todo rehearsal letters
                pass

    for gfhold in gfholds:
        if gfhold.find("f:clefID", namespaces=ns) is not None:
            clefID = gfhold.find("f:clefID", namespaces=ns).text
        # if handle_tempo:
        #     beatsPerMinute = root.xpath(f"/f:finale/f:options/f:playbackOptions/f:beatsPerMinute",
        #                                 namespaces=ns)
        #     edusPerBeat = root.xpath(f"/f:finale/f:options/f:playbackOptions/f:edusPerBeat", namespaces=ns)
        #     if beatsPerMinute is not None and edusPerBeat is not None:
        #         direction = SubElement(measure, "direction", placement='above')
        #         direction_type = SubElement(direction, "direction-type")
        #         if staff_id:
        #             SubElement(direction, "staff").text = str(staff_id)
        #         metronome = SubElement(direction_type, "metronome")
        #         type_name, nb_dots = calculate_type_and_dots(int(edusPerBeat[0].text))
        #         SubElement(metronome, "beat-unit").text = type_name
        #         SubElement(metronome, "per-minute").text = beatsPerMinute[0].text
        #     handle_tempo = False

        has_prev_frame = False
        for frame_num in range(1, 5):
            frame = gfhold.find(f"f:frame{frame_num}", namespaces=ns)
            if frame is not None:
                if has_prev_frame:
                    backup = SubElement(measure, "backup")
                    # todo is duration correctly calculated? Always start from start measure?
                    SubElement(backup, "duration").text = str(
                        (int(current_beats) * int(current_divbeat) * DIVISIONS) // 1024)
                frameSpec_cmper = frame.text
                process_frame(root, measure, frameSpec_cmper, frame_num, staff_id, key, transp_key_adjust,
                              transp_interval)
                has_prev_frame = True

    barline = SubElement(measure, "barline", location="right")
    bar_style = SubElement(barline, "bar-style")
    bar_style.text = translate_bar_style(barline_, bacRepBar, barEnding)
    if barEnding:
        SubElement(barline, "ending", number=str(ending_cnt), type='stop').text = f'{ending_cnt}.'
    else:
        ending_cnt = 0
    if bacRepBar:
        SubElement(barline, "repeat", direction='backward', winged='none')

    return clefID, handle_tempo


def process_entry(root, measure, entry, staff_id, voice, key, transp_key_adjust, transp_interval, tuplet_attributes):
    dura = int(entry.find("f:dura", namespaces=ns).text)
    is_note = entry.find("f:isNote", namespaces=ns) is not None
    noteDetail = entry.find("f:noteDetail", namespaces=ns) is not None
    lyricDetail = entry.find("f:lyricDetail", namespaces=ns) is not None
    articDetail = entry.find("f:articDetail", namespaces=ns) is not None
    if noteDetail:
        note_alter_map = lookup_note_alter(root, entry.get("entnum"))
        if VERBOSE: print(f'note_alter_map = {note_alter_map}')
    else:
        note_alter_map = {}

    if articDetail:
        artic_details = lookup_artic_detail(root, entry.get("entnum"))
        if VERBOSE: print(f'artic_detail_map = {artic_details}')
    else:
        artic_details = []

    # what is beam for?
    beam = entry.find("f:beam", namespaces=ns) is not None
    graceNote = entry.find("f:graceNote", namespaces=ns) is not None
    tupletStart = entry.find("f:tupletStart", namespaces=ns) is not None

    smartShapeDetail = entry.find("f:smartShapeDetail", namespaces=ns) is not None
    if is_note:
        # numNotes = int(entry.find("f:numNotes", namespaces=ns).text)
        notes = entry.xpath("f:note", namespaces=ns)
        for idx, note_ in enumerate(notes):
            note = SubElement(measure, "note")
            if idx == 0:
                if lyricDetail:
                    lyric_details = lookup_lyric_details(root, entry.get("entnum"))
                    for lyric_detail in lyric_details:
                        lyric = SubElement(note, "lyric", name="verse", number=lyric_detail["number"])
                        SubElement(lyric, "syllabic").text = lyric_detail["syllabic"]
                        SubElement(lyric, "text").text = lyric_detail["text"]
                        if lyric_detail["extend"]:
                            SubElement(lyric, "extend")
            if idx > 0:
                SubElement(note, "chord")
            if graceNote:
                # todo add notation slur start and stop (target note) =  smartshape of type slurUp
                # todo determine when slash="yes"
                SubElement(note, "grace", slash="no")
            pitch = SubElement(note, "pitch")
            harm_lev = int(note_.find("f:harmLev", namespaces=ns).text)
            harm_alt = int(note_.find("f:harmAlt", namespaces=ns).text)
            enharmonic = note_alter_map[note_.get('id')]['enharmonic'] if note_.get('id') in note_alter_map else False
            step_value, alter_value, octave_value = calculate_step_alter_and_octave(harm_lev, harm_alt, key,
                                                                                    transp_key_adjust, transp_interval,
                                                                                    enharmonic)
            step = SubElement(pitch, "step")
            step.text = step_value
            if alter_value != 0:
                alter = SubElement(pitch, "alter")
                alter.text = str(alter_value)
            octave = SubElement(pitch, "octave")
            octave.text = str(octave_value)
            if not graceNote:
                duration = SubElement(note, "duration")
                duration.text = str((dura * DIVISIONS) // 1024)

            tie_start = note_.find("f:tieStart", namespaces=ns)
            tie_end = note_.find("f:tieEnd", namespaces=ns)

            if tie_start is not None:
                SubElement(note, "tie", type='start')
            if tie_end is not None:
                SubElement(note, "tie", type='stop')

            voice_elem = SubElement(note, "voice")
            voice_elem.text = str(voice)
            type_name, nb_dots = calculate_type_and_dots(dura)
            if type_name:  # type_name can be None if the dura is not supported
                type_elem = SubElement(note, "type")
                type_elem.text = type_name
                for _ in range(nb_dots):
                    SubElement(note, "dot")

            if staff_id:
                SubElement(note, "staff").text = str(staff_id)

            if idx == 0:
                notations = SubElement(note, "notations")
                if smartShapeDetail:
                    handleSmartShapeDetail(root, entry, notations)
                if tupletStart:
                    handleTupletStart(root, entry, notations, tuplet_attributes)
                if len(tuplet_attributes) > 0:
                    # todo handle symbolicDur != refDur
                    is_nested = len(tuplet_attributes) > 1
                    count_tuplet(tuplet_attributes, dura)
                    if VERBOSE: print(tuplet_attributes)
                    actual_notes = 1
                    normal_notes = 1
                    for attributes in tuplet_attributes:
                        actual_notes *= int(attributes['symbolicNum'])
                        normal_notes *= int(attributes['refNum'])
                        if attributes['count'] == int(attributes['symbolicNum']):
                            SubElement(notations, 'tuplet', number=attributes['number'], type='stop')
                            tuplet_attributes.remove(attributes)
                    time_modification = SubElement(note, "time-modification")
                    SubElement(time_modification, "actual-notes").text = str(actual_notes)
                    SubElement(time_modification, "normal-notes").text = str(normal_notes)
                    if is_nested:
                        normal_type, _ = calculate_type_and_dots(int(tuplet_attributes[0]['symbolicDur']))
                        SubElement(time_modification, "normal-type").text = normal_type

                if articDetail:
                    articulations = SubElement(notations, "articulations")
                    for art_detail in artic_details:
                        tag_name, type = translate_articualtion(art_detail['charMain'])
                        articulation = SubElement(articulations, tag_name)
                        if type:
                            articulation.set('type', type)

                # Remove empty notations element
                if len(notations.getchildren()) == 0:
                    note.remove(notations)

            reorder_children(note,
                             ["grace", "chord", "pitch", "unpitched", "rest", "cue", "duration", "tie", "instrument",
                              "footnote", "level", "voice", "type", "dot", "accidental", "time-modification", "stem",
                              "notehead", "notehead-text", "staff", "beam", "notations", "lyric", "play", "listen"
                              ]
                             )



    else:
        note = SubElement(measure, "note")
        SubElement(note, "rest")
        duration = SubElement(note, "duration")
        duration.text = str((dura * DIVISIONS) // 1024)
        voice_elem = SubElement(note, "voice")
        voice_elem.text = str(voice)
        type_name, nb_dots = calculate_type_and_dots(dura)
        if type_name:  # type_name can be None if the dura is not supported
            type_elem = SubElement(note, "type")
            type_elem.text = type_name
            for _ in range(nb_dots):
                SubElement(note, "dot")
            if staff_id:
                SubElement(note, "staff").text = str(staff_id)
        notations = SubElement(note, "notations")
        if smartShapeDetail:
            handleSmartShapeDetail(root, entry, notations)
        if tupletStart:
            handleTupletStart(root, entry, notations, tuplet_attributes)
        if len(tuplet_attributes) > 0:
            # todo handle symbolicDur != refDur
            is_nested = len(tuplet_attributes) > 1
            count_tuplet(tuplet_attributes, dura)
            if VERBOSE: print(tuplet_attributes)
            actual_notes = 1
            normal_notes = 1
            for attributes in tuplet_attributes:
                actual_notes *= int(attributes['symbolicNum'])
                normal_notes *= int(attributes['refNum'])
                if attributes['count'] == int(attributes['symbolicNum']):
                    SubElement(notations, 'tuplet', number=attributes['number'], type='stop')
                    tuplet_attributes.remove(attributes)
            time_modification = SubElement(note, "time-modification")
            SubElement(time_modification, "actual-notes").text = str(actual_notes)
            SubElement(time_modification, "normal-notes").text = str(normal_notes)
            if is_nested:
                normal_type, _ = calculate_type_and_dots(int(tuplet_attributes[0]['symbolicDur']))
                SubElement(time_modification, "normal-type").text = normal_type

        # Remove empty notations element
        if len(notations.getchildren()) == 0:
            note.remove(notations)

        reorder_children(note,
                         ["grace", "chord", "pitch", "unpitched", "rest", "cue", "duration", "tie", "instrument",
                          "footnote", "level", "voice", "type", "dot", "accidental", "time-modification", "stem",
                          "notehead", "notehead-text", "staff", "beam", "notations", "lyric", "play", "listen"
                          ]
                         )
    return tuplet_attributes
