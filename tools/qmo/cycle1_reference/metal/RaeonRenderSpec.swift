import Foundation
import simd

public struct RaeonRenderSpec: Codable {
    public let schema: String
    public let qmo_address: String
    public let manifold_id: String
    public let native_color: String
    public let native_color_value: Int
    public let generator_count: Int
    public let generators: [String]
    public let anchors: [Anchor]
    public let topological_edges: [[Int]]
    public let spline_edges: [SplineEdge]
    public let chirality_sign: Int
    public let resolution: ResolutionSpec
    public let bandwidth: BandwidthSpec
    public let field_shell: FieldShellSpec
    public let animation: AnimationSpec
    public let projection_3plus1plus1: ProjectionSpec
    public let deterministic_seed: UInt64
    public let render_states: [String]
    public let authority: String
}

public struct Anchor: Codable {
    public let generator: String
    public let position: [Float]
    public let chirality_parity: Int
    public let fractal_address: String
}

public struct SplineEdge: Codable {
    public let edge_id: Int
    public let a: Int
    public let b: Int
    public let p0: [Float]
    public let p1: [Float]
    public let p2: [Float]
    public let p3: [Float]
    public let curve_samples: Int
    public let ring_samples: Int
    public let tube_radius: Float
}

public struct ResolutionSpec: Codable {
    public let mean: Float
    public let curve_samples: Int
    public let ring_samples: Int
}

public struct BandwidthSpec: Codable {
    public let mean: Float
    public let tube_radius_scale: Float
}

public struct FieldShellSpec: Codable {
    public let enabled: Bool
    public let kernel: String
    public let sigma: Float
    public let iso_threshold: Float
    public let grid_resolution: Int
}

public struct AnimationSpec: Codable {
    public let energy_wave_number: Float
    public let energy_angular_frequency: Float
    public let emission_power: Float
    public let tap_pulse_decay: Float
    public let breath_frequency: Float
    public let vertex_displacement: Float
}

public struct ProjectionSpec: Codable {
    public let alpha: Float
    public let beta: Float
    public let tau_frequency: Float
    public let chi: Float
}
