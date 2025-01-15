'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import { signOut } from '@/auth';
import {
  HomeIcon,
  DocumentDuplicateIcon,
  CubeIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';

const links = [
  { name: 'Home', href: '/dashboard', icon: HomeIcon },
  { name: 'Items', href: '/dashboard/items', icon: CubeIcon },
  { name: 'Transactions', href: '/dashboard/transactions', icon: DocumentDuplicateIcon },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <nav className="flex flex-1 flex-row space-x-2 md:flex-col md:space-x-0 md:space-y-2">
          {links.map((link) => {
            const LinkIcon = link.icon;
            return (
              <Link
                key={link.name}
                href={link.href}
                className={clsx(
                  'flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3',
                  {
                    'bg-sky-100 text-blue-600': pathname === link.href,
                  },
                )}
              >
                <LinkIcon className="w-6" />
                <p className="hidden md:block">{link.name}</p>
              </Link>
            );
          })}
        </nav>
        <div className="flex flex-col justify-end">
          <button
            onClick={() => signOut()}
            className="flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-red-100 hover:text-red-600 md:flex-none md:justify-start md:p-2 md:px-3"
          >
            <ArrowRightOnRectangleIcon className="w-6" />
            <span className="hidden md:block">Log Out</span>
          </button>
        </div>
      </div>
    </div>
  );
} 