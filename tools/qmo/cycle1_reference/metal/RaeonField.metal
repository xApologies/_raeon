#include <metal_stdlib>
using namespace metal;

struct VertexOut {
    float4 position [[position]];
    float3 world;
    float arclength;
};

struct FieldUniforms {
    float time;
    float tapTime;
    float waveNumber;
    float angularFrequency;
    float emissionPower;
    float tapDecay;
    float displacement;
    float colorValue;
};

fragment half4 raeonFieldFragment(VertexOut in [[stage_in]],
                                  constant FieldUniforms& u [[buffer(0)]]) {
    float phase = u.waveNumber * in.arclength - u.angularFrequency * u.time;
    float wave = pow(0.5 + 0.5*cos(phase), 3.0);
    float dt = max(0.0, u.time - u.tapTime);
    float pulse = exp(-u.tapDecay * dt);
    float intensity = 0.18 + wave * u.emissionPower + pulse * 3.0;
    // Placeholder spectral gold. Production palette maps semantic color state separately.
    half3 rgb = half3(1.0h, 0.58h, 0.06h) * half(intensity);
    return half4(rgb, 1.0h);
}
