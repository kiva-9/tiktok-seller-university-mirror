import type { ComponentProps } from 'react';
import DefaultTheme, {
  Layout as DefaultLayout,
  getCustomMDXComponent,
} from '@/theme-default';

const VIDEO_HINT_RE = /(mime(?:\\?_|_)type=video(?:\\?_|_)mp4|\.mp4(?:[?#]|$)|\/video\/tos\/)/i;
const defaultMdxComponents = getCustomMDXComponent();
const DefaultA = defaultMdxComponents.a;

function normalizeVideoUrl(url: string) {
  return url.replace(/\\_/g, '_');
}

function isVideoLink(props: ComponentProps<'a'>) {
  const href = normalizeVideoUrl(String(props.href || ''));
  const text = props.children;

  return (
    typeof text === 'string' &&
    text.trim().includes('视频') &&
    VIDEO_HINT_RE.test(href)
  );
}

function VideoAwareLink(props: ComponentProps<'a'>) {
  if (!isVideoLink(props)) {
    return <DefaultA {...props} />;
  }

  const videoUrl = normalizeVideoUrl(String(props.href || ''));

  return (
    <span className="mirror-video-card">
      <video
        className="mirror-video-player"
        controls
        playsInline
        preload="metadata"
        src={videoUrl}
      >
        Seu navegador nao conseguiu carregar este video.
      </video>
      <span className="mirror-video-caption">
        <a href={videoUrl} target="_blank" rel="noopener noreferrer">
          Abrir video original
        </a>
      </span>
    </span>
  );
}

export const Layout = (props: ComponentProps<typeof DefaultLayout>) => {
  return (
    <DefaultLayout
      {...props}
      components={{
        ...props.components,
        a: VideoAwareLink,
      }}
    />
  );
};

export default {
  ...DefaultTheme,
  Layout,
};

export * from '@/theme-default';
