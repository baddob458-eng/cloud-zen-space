export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white flex items-center justify-center px-4">
      <div className="max-w-4xl mx-auto text-center space-y-8 animate-fade-in">
        <h1 className="text-5xl md:text-7xl font-bold leading-tight">
          All your apps and AI tools on one screen—simple, private, <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-500">unstoppable</span>.
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 max-w-2xl mx-auto">
          Stop switching tabs. Stop losing focus. Stay in your flow.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
          <a
            href="/signup"
            className="px-8 py-4 bg-green-500 hover:bg-green-400 rounded-lg font-semibold text-lg transition-all hover:scale-105 shadow-lg"
          >
            Get Started Free
          </a>
          <a
            href="/login"
            className="px-8 py-4 border border-gray-600 hover:border-gray-400 rounded-lg font-semibold text-lg transition-all hover:scale-105"
          >
            Sign In
          </a>
        </div>
        <p className="text-sm text-gray-500 pt-4">
          Optimized for desktop — mobile available when you need it.
        </p>
      </div>
    </div>
  );
}
