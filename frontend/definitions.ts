// This file contains type definitions for your data.
// It describes the shape of the data, and what data type each property should accept.
// For simplicity of teaching, we're manually defining these types.
// However, these types are generated automatically if you're using an ORM such as Prisma.
export type User = {
    id: string;
    name: string;
    email: string;
    password: string;
  };
  
  export type Category = {
    id: string;
    name: string;
    description: string;
  };
  
  export type Item = {
    id: string;
    name: string;
    description: string;
    quantity: number;
    category_id: string;
  };

  export type Transaction = {
    id: string;
    item_id: string;
    quantity_change: number;
    transaction_type: string;
    transaction_date: string;
    user_id: string;
  };

  
  // The database returns a number for amount, but we later format it to a string with the formatCurrency function
//   export type LatestInvoiceRaw = Omit<LatestInvoice, 'amount'> & {
//     amount: number;
//   };
  
  export type CategoriesTable = {
    id: string;
    name: string;
    description: string;
  };
  
  export type ItemsTable = {
    id: string;
    name: string;
    description: string;
    quantity: number;
    category_id: string;
  };
  
  export type TransactionsTable = {
    id: string;
    item_id: string;
    quantity_change: number;
    transaction_type: string;
    transaction_date: string;
    user_id: string;
  };

  export type LoginCredentials = {
    email: string;
    password: string;
  };

  export type RegisterCredentials = LoginCredentials & {
    confirm_password: string;
  };

  export type AuthResponse = {
    token: string;
    token_type: string;
    user: User;
  };