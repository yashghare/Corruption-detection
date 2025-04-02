import Navbar from './components/Navbar';
import HomePage from './components/HomePage';

export default function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow">
        <HomePage />
      </main>
      <footer className="bg-gray-800 text-white p-4 text-center">
        © {new Date().getFullYear()} Fraud Detection System
      </footer>
    </div>
  );
}