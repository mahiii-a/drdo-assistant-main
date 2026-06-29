function Navbar() {
  const username = localStorage.getItem("name") || "User";

  return (
    <div className="bg-white shadow rounded-xl p-4 mb-6 flex justify-between items-center">
      <h2 className="text-xl font-semibold">
        DRDO Intelligent Document Assistant
      </h2>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center">
          {username.charAt(0).toUpperCase()}
        </div>

        <span>{username}</span>
      </div>
    </div>
  );
}

export default Navbar;