import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, PlusCircle, FileText, ShoppingBag } from 'lucide-react';
import clsx from 'clsx';

import logo from '../assets/logo.jpg';

const Layout = ({ children }) => {
    const location = useLocation();

    const navItems = [
        { name: 'Dashboard', path: '/', icon: LayoutDashboard },
        { name: 'Create Bill', path: '/create', icon: PlusCircle },
        { name: 'View Bills', path: '/bills', icon: FileText },
    ];

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-900 border-r border-gray-800">
                <div className="p-6 border-b border-amber-700/30">
                    <div className="flex items-center gap-3">
                        <img
                            src={logo}
                            alt="Royal Vastram"
                            className="w-10 h-10 rounded-lg object-cover shadow-lg border-2 border-amber-500/50"
                        />
                        <div>
                            <h1 className="text-xl font-bold text-white tracking-wide" style={{ fontFamily: 'serif' }}>Royal Vastram</h1>
                            <p className="text-xs text-amber-500 uppercase tracking-widest">Saree Collection</p>
                        </div>
                    </div>
                </div>
                <nav className="p-4 space-y-2">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = location.pathname === item.path;

                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={clsx(
                                    "flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200",
                                    isActive
                                        ? "bg-amber-600 text-white shadow-lg shadow-amber-900/20"
                                        : "text-gray-400 hover:bg-gray-800 hover:text-white"
                                )}
                            >
                                <Icon className="w-5 h-5" />
                                {item.name}
                            </Link>
                        );
                    })}
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto">
                <header className="bg-white border-b border-gray-200 px-8 py-4">
                    <h2 className="text-xl font-semibold text-gray-800">
                        {navItems.find(i => i.path === location.pathname)?.name || 'Invoice'}
                    </h2>
                </header>
                <div className="p-8 max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
