import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import ApplicationReview from './pages/ApplicationReview';
import UserProfile from './pages/UserProfile';
import OnboardingGuide from './components/OnboardingGuide';
import AddCreditRequest from './pages/AddCreditRequest';
import About from './pages/About';
import ApiStatus from './pages/ApiStatus';

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-gray-100">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/application/:id" element={<ApplicationReview />} />
            <Route path="/profile" element={<UserProfile />} />
            <Route path="/add-credit-request" element={<AddCreditRequest />} />
            <Route path="/about" element={<About />} />
            <Route path="/api-status" element={<ApiStatus />} />

            {/* 404 */}
            <Route path="*" element={<h1>Not Found</h1>} />
          </Routes>
        </main>
        <Footer />
        <OnboardingGuide />
      </div>
    </Router>
  );
}
