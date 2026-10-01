"""The supported entry point for building The King's Last Stand."""
import argparse
from pipeline import build
from install_diagnostic import install
from editor_layout import prepare_editor_copy, update_northern_editor_runtime

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--install-test-map', '--install-diagnostic', dest='install_test_map', action='store_true', help='Install the current development build in the local Warcraft III test folder')
    parser.add_argument('--prepare-editor', action='store_true', help='Create a terrain work copy with disposable editor layout references')
    parser.add_argument('--northern-editor-map', help='Preserved DE editing copy for the explicit northern runtime handoff')
    parser.add_argument('--editor-output', help='New output path; existing outputs are refused')
    parser.add_argument('--editor-baseline', help='Original raw MPQ baseline for an extracted Forge folder')
    parser.add_argument('--forest-camps', action='store_true', help='Include the approved one-time forest camps in the editor handoff')
    parser.add_argument('--dress-forest', help='Apply catalog dressing to the currently open dedicated Forge folder')
    parser.add_argument('--forge-lock', help='Selected Forge MCP lockfile for live dressing')
    parser.add_argument('--racial-action', choices=('prepare','refresh','apply','package','audit'), help='Preservation-first racial construction/recruitment handoff')
    parser.add_argument('--racial-folder', help='New or prepared racial MCP work folder')
    parser.add_argument('--worker-page-prototype', action='store_true', help='Grant worker page buttons ONLY in the separate native-acceptance prototype')
    parser.add_argument('--import-market-layout', help='Import saved native shop moves by creation identity into the source catalog')
    parser.add_argument('--dress-countryside', help='Apply fitted countryside catalog to the dedicated open Forge folder')
    parser.add_argument('--countryside-editor-map', help='Saved countryside folder for targeted market/group/pathing handoff')
    parser.add_argument('--refine-countryside', action='store_true', help='Correct the completed first pass lookouts and drape new props to saved ground')
    parser.add_argument('--verify-countryside', help='Read-only package/terrain preservation checks for a countryside handoff')
    parser.add_argument('--countryside-folder', help='Applied countryside catalog folder for --verify-countryside')
    parser.add_argument('--prepare-hero-market', help='Baseline native map for preservation-first hero/market repairs')
    parser.add_argument('--hero-market-folder', help='New or prepared dedicated hero/market folder')
    parser.add_argument('--apply-hero-market', action='store_true', help='Apply prepared typed object corrections through Forge MCP')
    parser.add_argument('--package-hero-market', action='store_true', help='Package the completed MCP repairs and synchronized runtime')
    parser.add_argument('--refresh-hero-market', action='store_true', help='Refresh typed main/skin payloads after verified source refinements')
    parser.add_argument('--audit-hero-market', action='store_true', help='Read every hero skill and signature through MCP and capture display metadata')
    args = parser.parse_args()
    if args.racial_action:
        if not args.racial_folder:parser.error('--racial-folder is required')
        from racial_handoff import prepare,refresh,apply,package,audit
        if args.racial_action=='prepare':
            if not args.editor_baseline or not args.forge_lock:parser.error('Prepare requires --editor-baseline and --forge-lock')
            print(prepare(args.editor_baseline,args.racial_folder,args.forge_lock))
        elif args.racial_action=='refresh':print(refresh(args.racial_folder))
        elif args.racial_action=='apply':
            if not args.forge_lock:parser.error('Apply requires --forge-lock')
            print(apply(args.racial_folder,args.forge_lock))
        elif args.racial_action=='audit':
            if not args.forge_lock:parser.error('Audit requires --forge-lock')
            print(audit(args.racial_folder,args.forge_lock))
        else:
            if not args.editor_output:parser.error('Package requires --editor-output')
            print(package(args.racial_folder,args.editor_output,args.worker_page_prototype))
        raise SystemExit(0)
    if args.prepare_hero_market or args.apply_hero_market or args.package_hero_market or args.refresh_hero_market or args.audit_hero_market:
        if not args.hero_market_folder or sum(bool(x) for x in (args.prepare_hero_market,args.apply_hero_market,args.package_hero_market,args.refresh_hero_market,args.audit_hero_market)) != 1:
            parser.error('Choose one hero/market action with --hero-market-folder')
        from hero_market_handoff import prepare,apply_mcp,package,refresh_expected,audit_mcp
        if args.prepare_hero_market:
            print(prepare(args.prepare_hero_market,args.hero_market_folder))
        elif args.audit_hero_market:
            if not args.forge_lock:parser.error('MCP audit requires --forge-lock')
            print(audit_mcp(args.hero_market_folder,args.forge_lock))
        elif args.refresh_hero_market:
            print(refresh_expected(args.hero_market_folder))
        elif args.apply_hero_market:
            if not args.forge_lock:parser.error('MCP application requires --forge-lock')
            print(apply_mcp(args.hero_market_folder,args.forge_lock))
        else:
            if not args.editor_output:parser.error('Packaging requires --editor-output')
            print(package(args.hero_market_folder,args.editor_output))
        raise SystemExit(0)
    if args.refine_countryside and not args.dress_countryside:
        parser.error('--refine-countryside requires --dress-countryside')
    if args.verify_countryside:
        if not args.countryside_folder or not args.editor_baseline:
            parser.error('Countryside verification requires --countryside-folder and --editor-baseline')
        from countryside_verify import verify_countryside
        print(verify_countryside(args.editor_baseline,args.verify_countryside,args.countryside_folder))
        raise SystemExit(0)
    if args.import_market_layout:
        if args.dress_countryside or args.countryside_editor_map or args.northern_editor_map or args.install_test_map or args.prepare_editor or args.dress_forest:
            parser.error('Market import must run separately before building the editor handoff')
        from editor_layout import import_market_layout
        print(import_market_layout(args.import_market_layout))
        raise SystemExit(0)
    if args.dress_countryside:
        if not args.forge_lock or args.northern_editor_map or args.countryside_editor_map or args.install_test_map or args.prepare_editor or args.dress_forest:
            parser.error('Live countryside dressing requires --forge-lock and a dedicated folder only')
        from forge_countryside import apply_countryside
        print(apply_countryside(args.forge_lock,args.dress_countryside,args.refine_countryside))
        raise SystemExit(0)
    if args.countryside_editor_map:
        if not args.editor_output or not args.editor_baseline or args.northern_editor_map or args.forest_camps or args.prepare_editor or args.install_test_map or args.dress_forest:
            parser.error('Countryside handoff requires --editor-output/--editor-baseline and cannot install or regenerate terrain')
        print(update_northern_editor_runtime(args.countryside_editor_map,args.editor_output,args.editor_baseline,countryside=True))
        raise SystemExit(0)
    if args.dress_forest:
        if not args.forge_lock or args.northern_editor_map or args.install_test_map or args.prepare_editor:
            parser.error('Live forest dressing requires --forge-lock and a dedicated folder only')
        from forge_forest import apply_forest
        print(apply_forest(args.forge_lock,args.dress_forest))
        raise SystemExit(0)
    if args.northern_editor_map:
        if not args.editor_output or args.prepare_editor or args.install_test_map:
            parser.error('Northern editor handoff requires --editor-output and cannot install or regenerate terrain')
        print(update_northern_editor_runtime(args.northern_editor_map, args.editor_output, args.editor_baseline, args.forest_camps))
        raise SystemExit(0)
    manifest = build()
    if args.prepare_editor:
        prepare_editor_copy(manifest)
    if args.install_test_map:
        install(manifest)
