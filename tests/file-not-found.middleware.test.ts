import { describe, it, expect, vi } from 'vitest';
import { fileNotFoundMiddleware, FileNotFoundError } from '../src/middleware/file-not-found.middleware';
import { Request, Response, NextFunction } from 'express';

describe('fileNotFoundMiddleware', () => {
  it('should handle FileNotFoundError with 404 status', () => {
    // Create mock request, response, and next function
    const mockReq = {} as Request;
    const mockJson = vi.fn();
    const mockStatus = vi.fn().mockReturnValue({ json: mockJson });
    const mockRes = {
      status: mockStatus
    } as unknown as Response;
    const mockNext = vi.fn() as unknown as NextFunction;

    // Create a FileNotFoundError
    const error = new FileNotFoundError('Test file not found');

    // Call middleware
    fileNotFoundMiddleware(error, mockReq, mockRes, mockNext);

    // Verify status and json methods were called correctly
    expect(mockStatus).toHaveBeenCalledWith(404);
    expect(mockJson).toHaveBeenCalledWith({
      error: 'File not found',
      message: 'The requested file could not be located.'
    });

    // Verify next was not called
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('should pass non-FileNotFoundError to next middleware', () => {
    // Create mock request, response, and next function
    const mockReq = {} as Request;
    const mockJson = vi.fn();
    const mockStatus = vi.fn().mockReturnValue({ json: mockJson });
    const mockRes = {
      status: mockStatus,
      json: mockJson
    } as unknown as Response;
    const mockNext = vi.fn() as unknown as NextFunction;

    // Create a generic error
    const error = new Error('Generic error');

    // Call middleware
    fileNotFoundMiddleware(error, mockReq, mockRes, mockNext);

    // Verify next was called with the error
    expect(mockNext).toHaveBeenCalledWith(error);
    expect(mockStatus).not.toHaveBeenCalled();
  });

  it('should create FileNotFoundError with correct properties', () => {
    const errorMessage = 'Specific file not found';
    const error = new FileNotFoundError(errorMessage);

    expect(error).toBeInstanceOf(Error);
    expect(error.name).toBe('FileNotFoundError');
    expect(error.message).toBe(errorMessage);
  });
});