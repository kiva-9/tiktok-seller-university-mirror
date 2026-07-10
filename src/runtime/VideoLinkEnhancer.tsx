import { useLocation } from '@rspress/runtime';
import { useEffect } from 'react';

const VIDEO_HINT_RE = /(mime(?:\\?_|_)type=video(?:\\?_|_)mp4|\.mp4(?:[?#]|$)|\/video\/tos\/)/i;

function normalizeVideoUrl(url: string) {
  return url.replace(/\\_/g, '_');
}

function isVideoAnchor(anchor: HTMLAnchorElement) {
  const text = anchor.textContent?.trim() || '';
  const href = normalizeVideoUrl(anchor.getAttribute('href') || anchor.href || '');

  return text.includes('视频') && VIDEO_HINT_RE.test(href);
}

function createVideoCard(anchor: HTMLAnchorElement) {
  const videoUrl = normalizeVideoUrl(anchor.getAttribute('href') || anchor.href);

  const card = document.createElement('figure');
  card.className = 'mirror-video-card';

  const video = document.createElement('video');
  video.className = 'mirror-video-player';
  video.controls = true;
  video.preload = 'metadata';
  video.playsInline = true;
  video.src = videoUrl;
  video.textContent = 'Seu navegador nao conseguiu carregar este video.';

  const caption = document.createElement('figcaption');
  caption.className = 'mirror-video-caption';

  const link = document.createElement('a');
  link.href = videoUrl;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.textContent = 'Abrir video original';

  caption.appendChild(link);
  card.appendChild(video);
  card.appendChild(caption);

  return card;
}

function enhanceVideoLinks() {
  const doc = document.querySelector('.rspress-doc');
  if (!doc) return;

  const anchors = Array.from(doc.querySelectorAll<HTMLAnchorElement>('a[href]'));
  for (const anchor of anchors) {
    if (anchor.dataset.mirrorVideoEnhanced === 'true') continue;
    if (!isVideoAnchor(anchor)) continue;

    anchor.dataset.mirrorVideoEnhanced = 'true';
    const card = createVideoCard(anchor);
    const paragraph = anchor.closest('p');

    if (paragraph && (paragraph.textContent || '').replace(/\s/g, '') === '🎬视频') {
      paragraph.replaceWith(card);
    } else {
      anchor.replaceWith(card);
    }
  }
}

export default function VideoLinkEnhancer() {
  const { pathname } = useLocation();

  useEffect(() => {
    if (typeof window === 'undefined') return;

    let frame = window.requestAnimationFrame(enhanceVideoLinks);
    const observer = new MutationObserver(() => {
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(enhanceVideoLinks);
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

    return () => {
      window.cancelAnimationFrame(frame);
      observer.disconnect();
    };
  }, [pathname]);

  return null;
}
