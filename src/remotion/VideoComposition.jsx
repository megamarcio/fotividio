import {
  AbsoluteFill,
  Sequence,
  Video,
  Img,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from 'remotion';

export const VideoComposition = ({ clips, subtitles, transitions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  let currentFrame = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {clips.map((clip, i) => {
        const startFrame = currentFrame;
        const durationFrames = Math.round((clip.duration || 5) * fps);
        currentFrame += durationFrames;

        const opacity =
          transitions === 'fade'
            ? interpolate(
                frame,
                [startFrame, startFrame + 15, startFrame + durationFrames - 15, startFrame + durationFrames],
                [0, 1, 1, 0],
                { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
              )
            : 1;

        const scale =
          clip.effect === 'zoom'
            ? interpolate(frame, [startFrame, startFrame + durationFrames], [1, clip.zoomFactor || 1.3], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              })
            : 1;

        return (
          <Sequence key={i} from={startFrame} durationInFrames={durationFrames}>
            <AbsoluteFill style={{ opacity, transform: `scale(${scale})` }}>
              {clip.type === 'video' && <Video src={clip.src} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
              {clip.type === 'image' && <Img src={clip.src} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />}
            </AbsoluteFill>
          </Sequence>
        );
      })}

      {subtitles.map((sub, i) => {
        const startFrame = Math.round(sub.start * fps);
        const durationFrames = Math.round((sub.end - sub.start) * fps);
        const popIn = spring({ frame: frame - startFrame, fps, config: { damping: 12 } });

        return (
          <Sequence key={`sub-${i}`} from={startFrame} durationInFrames={durationFrames}>
            <AbsoluteFill
              style={{
                justifyContent: 'flex-end',
                alignItems: 'center',
                paddingBottom: 80,
              }}
            >
              <div
                style={{
                  background: 'rgba(0,0,0,0.7)',
                  color: 'white',
                  padding: '12px 24px',
                  borderRadius: 8,
                  fontSize: 32,
                  fontFamily: 'Arial, sans-serif',
                  fontWeight: 'bold',
                  transform: `scale(${popIn})`,
                  maxWidth: '80%',
                  textAlign: 'center',
                }}
              >
                {sub.text}
              </div>
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
