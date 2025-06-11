import { Request, Response, NextFunction } from 'express';

/**
 * Middleware to handle file not found errors
 * @param err - Error object
 * @param req - Express request object
 * @param res - Express response object
 * @param next - Next middleware function
 */
export const fileNotFoundMiddleware = (
  err: Error, 
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
  // Check if the error is a file not found error
  if (err.name === 'FileNotFoundError') {
    // Send a 404 response with a generic error message
    return res.status(404).json({
      error: 'File not found',
      message: 'The requested file could not be located.'
    });
  }

  // If not a file not found error, pass to next error handler
  next(err);
};

/**
 * Custom error class for file not found scenarios
 */
export class FileNotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'FileNotFoundError';
  }
}