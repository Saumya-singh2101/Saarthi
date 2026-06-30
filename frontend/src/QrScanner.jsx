import { useEffect } from "react";
import { Html5QrcodeScanner } from "html5-qrcode";

export default function QrScanner({ onScan, onClose }) {
  useEffect(() => {
    const scanner = new Html5QrcodeScanner(
      "qr-reader",
      { fps: 10, qrbox: { width: 220, height: 220 } },
      false
    );

    scanner.render(
      (decodedText) => {
        scanner.clear().catch(() => {});
        onScan(decodedText);
      },
      () => {} // ignore per-frame decode errors (noisy, harmless)
    );

    return () => { scanner.clear().catch(() => {}); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="qr-overlay">
      <div className="qr-modal">
        <div className="qr-modal-head">
          <h3>Scan Health Card</h3>
          <button className="qr-close" onClick={onClose}>✕</button>
        </div>
        <div id="qr-reader" />
        <p className="hint">Point the camera at the card's QR code.</p>
      </div>
    </div>
  );
}