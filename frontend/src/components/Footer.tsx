export default function Footer() {
  return (
    <footer className="site-footer" id="contact">
      <div className="container footer-container">
        <div className="footer-brand">
          <i className="fas fa-language"></i>
          <span>LibreTranslate</span>
        </div>

        <div className="footer-grid">
          <div className="footer-col">
            <h4>Company</h4>
            <p><strong>Shravani Limited</strong></p>
            <p>
              82a, James Carter Road<br/>
              Mildenhall, IP28 7DE, UK
            </p>
            <p>Company No: 15862442</p>
          </div>

          <div className="footer-col">
            <h4>Contact</h4>
            <p>
              <i className="fas fa-envelope"></i>
              <a href="mailto:info@shravani.group">info@shravani.group</a>
            </p>
            <p>
              <i className="fas fa-phone"></i>
              <a href="tel:+447453541117">+44 7453 541 117</a>
            </p>
          </div>

          <div className="footer-col">
            <h4>Location</h4>
            <p>
              <i className="fas fa-location-dot"></i>
              <span>United Kingdom</span>
            </p>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} Shravani Limited. All rights reserved.</span>
        </div>
      </div>
    </footer>
  );
}
