# --- Stage 1: Build Stage ---
# Use a full Python image to install dependencies, including those that need to be compiled.
FROM python:3.11 as builder

# Set the working directory
WORKDIR /app

# Upgrade pip and install wheel to create binary distributions
RUN pip install --upgrade pip wheel

# Copy the requirements file
COPY requirements.txt .

# Create a wheelhouse for all dependencies
# This pre-compiles packages, speeding up the final build and avoiding the need for build tools in the final image.
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# --- Stage 2: Final Production Stage ---
# Use a slim Python image for a smaller final image size.
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Create a non-root user for security best practices
RUN addgroup --system app && adduser --system --group app

# Copy the pre-compiled wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install the dependencies from the wheelhouse
RUN pip install --no-cache /wheels/*

# Copy your application code from the 'app' directory into the container
COPY ./app ./app

# Change ownership of the files to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port that the application will run on
EXPOSE 8000

# Set the main command that will always run when the container starts
ENTRYPOINT ["uvicorn"]

# Set the default arguments for the ENTRYPOINT. These can be overridden at runtime.
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]
