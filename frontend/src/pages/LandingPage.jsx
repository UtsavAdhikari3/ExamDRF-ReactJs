
const LandingPage = () => {
    return (
      <div className="landing-page-container">
        {/* Header section with the main call to action */}
        <header className="hero-section">
          <div className="hero-content">
            <h1>Master Your Exams with Our Platform</h1>
            <p>
              Unlock your full potential with our comprehensive suite of practice and live exams. Prepare,
              perform, and succeed like never before.
            </p>
            <div className="cta-buttons">
              <button className="btn btn-primary">Start Your Free Trial</button>
              <button className="btn btn-secondary">Explore Features</button>
            </div>
          </div>
        </header>
  
        {/* Main content section highlighting key features */}
        <main className="main-content">
          {/* Features section with cards */}
          <section className="features-section">
            <h2>Key Features</h2>
            <div className="features-grid">
              {/* Practice Exams Card */}
              <div className="feature-card">
                <span className="icon">📚</span>
                <h3>Practice Exams</h3>
                <p>
                  Take unlimited practice exams tailored to your subject. Get instant feedback,
                  detailed performance analysis, and track your progress over time.
                </p>
              </div>
  
              {/* Live Exams Card */}
              <div className="feature-card">
                <span className="icon">⏳</span>
                <h3>Live Exams</h3>
                <p>
                  Experience real-time exams in a simulated environment. Compete with others,
                  test your speed and accuracy, and get ready for the real thing.
                </p>
              </div>
            </div>
          </section>
  
          {/* Call-to-action section */}
          <section className="cta-section">
            <h2>Ready to Get Started?</h2>
            <p>Join thousands of students who are acing their exams with our platform. Sign up today!</p>
            <button className="btn btn-primary">Sign Up Now</button>
          </section>
        </main>
  
        {/* Footer section */}
        <footer className="footer">
          <p>&copy; 2024 Exam Platform. All rights reserved.</p>
        </footer>
      </div>
    );
  };

  export default LandingPage