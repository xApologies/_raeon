// Only source availability changed. Gameplay values remain protected by the
// checkpoint-0003 comparison and the continuity regression suite.
export const remainingCycle1Sources = [
  'Genesis mathematics', 'Chirality mathematics', 'Propagation mathematics',
  'Broader QMO definitions/API beyond imported Cycle-1 game profile',
  'Closure operators beyond imported Cycle-1 game profile',
  'Transduction mathematics/API',
  'Generator and derived-QMO RenderSpecs beyond the supplied 60 base specs',
  'Blender-facing Generator/derived geometry references not supplied',
  'Higher-dimensional projection mathematics'
];
export const previousCycle1Sources = [
  'Genesis mathematics','Chirality mathematics','Propagation mathematics',
  'QMO definitions and API','Closure operators','Transduction mathematics/API',
  '60 base Local Manifold QMOs','343 fusion-derived Local Manifold QMOs',
  '1,691 Emergent Field QMOs','Deterministic RenderSpec/API packages',
  'Field Generator QMO data','Complete 2,094-object QMO atlas',
  'Cycle Generation Constitution','Blender-facing manifold atlas/reference material',
  'Higher-dimensional projection mathematics'
];
export function projectBeforeCycle1Import(state) {
  const s=structuredClone(state);
  // Revert only the four authorized availability transitions for comparison.
  s.qmo_inventory.status='SOURCE_IMPORT_REQUIRED';
  s.qmo_inventory.objects_imported=false;
  s.rendering_direction.qmo_renderspec_api_packages='SOURCE_IMPORT_REQUIRED';
  s.cycle_production_direction.existing_source_package='SOURCE_IMPORT_REQUIRED';
  s.source_import_required=[...previousCycle1Sources];
  return s;
}
