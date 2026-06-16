import { Composition } from 'remotion';
import { VideoComposition } from './VideoComposition';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="FotiVidio"
        component={VideoComposition}
        durationInFrames={30 * 30}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          clips: [],
          subtitles: [],
          transitions: 'fade',
        }}
      />
    </>
  );
};
