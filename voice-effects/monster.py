# Monster voice
effects.apply_frequency_filter(300, 'lowpass')
effects.change_formants(0.7)
effects.add_distortion(gain=2.0, threshold=0.3)