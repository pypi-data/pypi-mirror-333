"""
Integration with lmfit's Model class.
"""

from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np

try:
    import lmfit
except ImportError:
    raise ImportError("lmfit is required for this functionality. " "Please install it with `pip install lmfit`.")

import zeroguess


class Model(lmfit.Model):
    """Enhanced version of lmfit.Model with automatic parameter estimation.

    This class extends lmfit's Model class to provide automatic initial parameter
    estimation using ZeroGuess when the original model doesn't implement guess().

    Example:
        ```python
        import numpy as np
        from zeroguess.integration import ZeroGuessModel

        def gaussian(x, amplitude, center, width):
            return amplitude * np.exp(-(x - center)**2 / (2 * width**2))

        # Define sampling points for training
        x_sampling = np.linspace(-10, 10, 100)

        # Create model with automatic parameter estimation
        model = ZeroGuessModel(
            gaussian,
            independent_vars_sampling={
                'x': x_sampling
            },
            estimator_settings={
                'architecture': 'mlp',  # Optional: Select MLP architecture
                'architecture_params': {  # Optional: Architecture-specific parameters
                    'activation': 'relu'
                }
            }
        )

        # Set parameter bounds (will be automatically used for parameter estimation)
        model.set_param_hint('amplitude', min=0, max=10)
        model.set_param_hint('center', min=-5, max=5)
        model.set_param_hint('width', min=0.1, max=2)

        # Fit data with automatic parameter estimation
        result = model.fit(y_data, x=x_data)
        ```

    Alternative with param_ranges specified directly:
        ```python
        # Create model with automatic parameter estimation using explicit param_ranges
        model = ZeroGuessModel(
            gaussian,
            param_ranges={
                'amplitude': (0, 10),
                'center': (-5, 5),
                'width': (0.1, 2)
            },
            independent_vars_sampling={
                'x': x_sampling
            },
            estimator_settings={
                'architecture': 'mlp',
                'architecture_params': {
                    'activation': 'relu'
                }
            }
        )

        # Fit data with automatic parameter estimation
        result = model.fit(y_data, x=x_data)
        ```
    """

    def __init__(
        self,
        fit_func: Callable,
        param_ranges: Optional[Dict[str, Tuple[float, float]]] = None,
        independent_vars_sampling: Optional[Dict[str, np.ndarray]] = None,
        estimator_settings: Dict[str, Any] = None,
        **kwargs,
    ):
        """Initialize the enhanced Model with parameter estimation capability.

        Args:
            fit_func: The model function to be wrapped
            param_ranges: Dictionary mapping parameter names to (min, max) tuples. If
                not provided, bounds will be extracted from parameter hints.
            independent_vars_sampling: Dictionary mapping independent variable names
                to arrays of sampling points for training
            estimator_settings: Dictionary containing settings for the estimator, such as:
                - architecture: Name of the neural network architecture to use (e.g., 'mlp', 'cnn')
                - architecture_params: Dictionary of architecture-specific parameters
                - Other estimator settings
            **kwargs: Additional keyword arguments passed to lmfit.Model
        """
        # Initialize the parent lmfit.Model
        super().__init__(fit_func, **kwargs)

        # Store ZeroGuess-specific parameters
        self.param_ranges = param_ranges
        self.independent_vars_sampling = independent_vars_sampling
        self._estimator = None

        self.estimator_settings = estimator_settings if estimator_settings is not None else {}

        # Check if this model has a guess method from the parent class
        self._has_parent_guess = self._has_custom_guess_method()

        # If parameter ranges are provided, initialize and train the estimator immediately
        if param_ranges is not None and independent_vars_sampling is not None:
            self._initialize_estimator()

    def _has_custom_guess_method(self) -> bool:
        """Check if the parent class has a custom guess method implementation.

        Returns:
            True if the parent class has a custom guess method, False otherwise
        """
        # Get the guess method from the parent class
        parent_guess = super(Model, self).guess

        # Check if it's the default implementation or a custom one
        # The default implementation in lmfit.Model raises NotImplementedError
        try:
            # Create minimal arguments to test the method
            x = np.linspace(0, 1, 10)
            y = np.zeros_like(x)
            parent_guess(y, x=x)
            return True
        except NotImplementedError:
            return False
        except Exception:
            # If it fails for other reasons, assume it has a custom implementation
            # that might work with proper data
            return True

    def _extract_bounds_from_params(self, params: lmfit.Parameters) -> Dict[str, Tuple[float, float]]:
        """Extract parameter bounds from lmfit Parameters object.

        Args:
            params: lmfit Parameters object

        Returns:
            Dictionary mapping parameter names to (min, max) tuples

        Raises:
            ValueError: If any parameter is missing min or max bounds
        """
        param_ranges = {}

        for param_name, param in params.items():
            # Check if both min and max are defined for this parameter
            if param.min is None or param.max is None:
                raise ValueError(
                    f"Parameter '{param_name}' must have both min and max bounds defined. "
                    f"Use model.set_param_hint('param_name', min=..., max=...) to set bounds on parameters. "
                    f"If you want to automatically extract bounds from params, use Model(param_ranges=None)."
                )

            # Ensure bounds are in a valid range (min < max)
            if param.min >= param.max:
                raise ValueError(f"Parameter '{param_name}' has invalid bounds: min ({param.min}) >= max ({param.max})")

            param_ranges[param_name] = (param.min, param.max)

        return param_ranges

    def _initialize_estimator(self, **train_kwargs):
        """Initialize and train the parameter estimator."""
        try:

            if not self.param_ranges:
                try:
                    params = super().make_params()
                    extracted_param_ranges = self._extract_bounds_from_params(params)
                    self.param_ranges = extracted_param_ranges
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to extract parameter bounds or train estimator: {str(e)}. "
                        f"Parameter estimation cannot proceed without valid bounds."
                        f"Use model.set_param_hint('param_name', min=..., max=...) to set bounds on parameters."
                    )

            if self.independent_vars_sampling is None:
                raise RuntimeError("Parameter estimation cannot proceed without independent variables.")

            # Create or load estimator
            self._estimator = zeroguess.create_estimator(
                function=self.func,
                param_ranges=self.param_ranges,
                independent_vars_sampling=self.independent_vars_sampling,
                # # Load if snapshot_path is provided
                # snapshot_path=self.estimator_settings.get("snapshot_path", None),
                **self.estimator_settings,
            )

            # Train the estimator
            if self._estimator.is_trained:
                print("Estimator is already trained. Skipping training.")
            else:
                self._estimator.train(**train_kwargs)

        except Exception as e:
            # If initialization or training fails, log the error and set estimator to None

            self._estimator = None

            raise RuntimeError(f"Failed to initialize or train parameter estimator: {str(e)}. ")

    def zeroguess_train(self, device=None, **train_kwargs):
        """Train the parameter estimator.

        This method explicitly trains or retrains the parameter estimator.

        Args:
            device: Device to use for training (e.g., 'cpu', 'cuda')
            **train_kwargs: Additional keyword arguments for training
        """
        if self._estimator is None:
            self._initialize_estimator(device=device, **train_kwargs)
        else:
            self._estimator.train(**train_kwargs)

    def guess(self, data, **kwargs) -> lmfit.Parameters:  # noqa: C901
        """Guess initial parameter values based on data.

        This method provides a ZeroGuess-based implementation of the guess method
        when the original Model class doesn't implement one.

        Args:
            data: Array of data (dependent variable) to use for guessing
            **kwargs: Additional keyword arguments, must contain the independent
                      variable(s) used during fitting.

        Returns:
            lmfit Parameters object with initial guesses

        Raises:
            ValueError: If required independent variables are missing
            RuntimeError: If parameter estimation fails or if bounds cannot be extracted
        """

        # If the parent class has a custom guess implementation, use it
        if self._has_parent_guess:
            return super().guess(data, **kwargs)

        # Extract independent variables from kwargs
        if len(self.independent_vars) != 1:
            raise NotImplementedError("Currently only supports models with one independent variable")

        # Get the independent variable (typically 'x')
        indep_var_name = self.independent_vars[0]
        if indep_var_name not in kwargs:
            raise ValueError(f"Independent variable '{indep_var_name}' must be provided")

        x_data = kwargs[indep_var_name]

        # Create parameters - IMPORTANT: For test_guess_method_success, we need to use the
        # latest parameters with bounds, not create new ones
        params = super().make_params()

        # Handle the case where estimator not initialized
        if self._estimator is None:
            # Initialize and train estimator
            self._initialize_estimator()

        # If estimator is available, use it to guess parameters
        if self._estimator is not None:
            try:
                # Use the estimator to predict initial parameters
                estimated_params = self._estimator.predict(x_data, data)

                # Update parameter values with estimated values
                for name, value in estimated_params.items():
                    if name in params:
                        params[name].set(value=value)
            except Exception as e:
                # Raise an exception instead of warning
                raise RuntimeError(
                    f"Parameter estimation failed: {str(e)}. " f"Unable to guess initial parameter values."
                )

        return params

    def fit(
        self,
        data: np.ndarray,
        params: Optional[lmfit.Parameters] = None,
        weights: Optional[np.ndarray] = None,
        method: Optional[str] = "leastsq",
        **kwargs,
    ) -> lmfit.model.ModelResult:
        """Fit the model to data with automatic parameter estimation if needed.

        This method extends lmfit.Model.fit by using our guess() method when needed,
        which will use ZeroGuess's parameter estimation capabilities.

        Args:
            data: The data to fit
            params: Parameters for the fit (optional, will be estimated if not provided)
            weights: Weights for the fit (optional)
            method: Fitting method (defaults to 'leastsq')
            **kwargs: Additional keyword arguments for the fit
                      including independent variables

        Returns:
            ModelResult from the fit
        """
        # Ensure method is not None for parent call
        if method is None:
            method = "leastsq"

        # Call the parent fit method, which will use our guess() method if params is None
        return super().fit(data, params, weights, method, **kwargs)


# Create alias for easier imports
__all__ = ["Model"]
